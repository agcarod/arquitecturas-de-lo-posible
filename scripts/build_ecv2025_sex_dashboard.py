#!/usr/bin/env python3
"""Reproduce sex composition, selector estimates, and women-only sensitivity.

Run from a directory containing the five original ECV 2025 module ZIP files:
  python build_ecv2025_sex_dashboard.py /path/to/five-zips

Only aggregate files are written to the repository; microdata are never copied.
Uses FEX_C and first-order Taylor linearization by ESTRATO2020/SEGMENTO.
"""
from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
OUT = Path(__file__).resolve().parents[1] / "data"
KEY = ["DIRECTORIO", "SECUENCIA_P", "ORDEN"]
HK = KEY[:2]
GROUPS = [
    ("study_and_work", "Estudian y trabajan"),
    ("study_no_occupation", "Estudiantes sin ocupación"),
    ("occupied_no_study", "Ocupados sin estudiar"),
    ("home_primary", "Oficios del hogar como actividad principal"),
    ("searched_elsewhere", "Búsqueda reciente de empleo (resto)"),
    ("other", "Otras situaciones"),
]
AGE_BANDS = [(18, 21, "18–21"), (22, 25, "22–25"), (26, 28, "26–28")]


def read_module(pattern: str, cols: list[str]) -> pd.DataFrame:
    matches = list(ROOT.glob(pattern))
    if len(matches) != 1:
        raise FileNotFoundError(f"Se esperaba un ZIP para {pattern}; encontrados: {matches}")
    with zipfile.ZipFile(matches[0]) as archive:
        name = next(n for n in archive.namelist() if n.lower().endswith(".csv"))
        data = pd.read_csv(archive.open(name), sep=";", decimal=",", encoding="latin1", usecols=cols)
    print(f"{matches[0].name}: {len(data):,} filas usadas")
    return data


def load_data() -> pd.DataFrame:
    c = read_module("*Caracteristicas_composicion_hogar-2025.zip", KEY + ["P6040", "P6020", "P1895", "P3175", "P1905"])
    w = read_module("*Fuerza_trabajo2025.zip", KEY + ["P6240", "P6250", "P6260", "P6270", "P6280"])
    e = read_module("*Educacion-2025.zip", KEY + ["P8586"])
    s = read_module("*Variables_diseno_muestral-2025.zip", KEY + ["SEGMENTO", "ESTRATO2020", "FEX_C"])
    h = read_module("*Condiciones_vida_hogar_tenencia_bienes-2025.zip", ["DIRECTORIO", "SECUENCIA_ENCUESTA", "SECUENCIA_P", "ORDEN", "P9090"])
    assert h.ORDEN.eq(h.SECUENCIA_ENCUESTA).all() and h.SECUENCIA_P.eq(1).all()
    h = h.drop(columns=["SECUENCIA_P", "SECUENCIA_ENCUESTA"]).rename(columns={"ORDEN": "SECUENCIA_P"})
    assert not h.duplicated(HK).any()
    y = c[c.P6040.between(18, 28)].copy()
    for part, key in [(w, KEY), (e, KEY), (s, KEY), (h, HK)]:
        y = y.merge(part, on=key, how="left", validate="one_to_one" if key == KEY else "many_to_one", indicator=True)
        assert y._merge.eq("both").all(), y._merge.value_counts().to_dict()
        y = y.drop(columns="_merge")
    assert len(y) == 35776 and y.P9090.isin([1, 2, 3]).all() and y.FEX_C.gt(0).all()
    assert y.P6020.isin([1, 2]).all(), y.P6020.value_counts(dropna=False).to_dict()
    y["work"] = (y.P6240 == 1) | y[["P6250", "P6260", "P6270"]].eq(1).any(axis=1)
    y["study"] = y.P8586.eq(1)
    y["group"] = np.select(
        [y.study & y.work, y.study & ~y.work, ~y.study & y.work,
         ~y.study & ~y.work & y.P6240.eq(4),
         ~y.study & ~y.work & y.P6280.eq(1)],
        ["study_and_work", "study_no_occupation", "occupied_no_study", "home_primary", "searched_elsewhere"],
        default="other",
    )
    y["income_sufficient"] = y.P9090.ge(2)
    y["age_band"] = pd.cut(y.P6040, [17, 21, 25, 28], labels=[x[2] for x in AGE_BANDS])
    return y


def design_index(y: pd.DataFrame) -> pd.MultiIndex:
    psu = y[["ESTRATO2020", "SEGMENTO"]].drop_duplicates()
    return pd.MultiIndex.from_frame(psu)


def ratio_estimate(y: pd.DataFrame, mask: pd.Series, col: str, psus: pd.MultiIndex):
    a = y.loc[mask, ["ESTRATO2020", "SEGMENTO", "FEX_C", col]].dropna().copy()
    denom = a.FEX_C.sum()
    if not len(a) or denom <= 0:
        return None
    est = float((a.FEX_C * a[col].astype(float)).sum() / denom)
    a["u"] = a.FEX_C * (a[col].astype(float) - est) / denom
    u = a.groupby(["ESTRATO2020", "SEGMENTO"]).u.sum().reindex(psus, fill_value=0)
    return est, u, int(len(a))


def se_taylor(u: pd.Series) -> float:
    by_stratum = u.groupby(level=0).agg(["count", "var"])
    return float(np.sqrt((by_stratum["count"] * by_stratum["var"].fillna(0)).sum()))


def estimate_json(y: pd.DataFrame, mask: pd.Series, col: str, psus: pd.MultiIndex, scale=1.0):
    result = ratio_estimate(y, mask, col, psus)
    if result is None:
        return None
    value, u, n = result
    se = se_taylor(u)
    return {"estimate": round(value * scale, 4), "ci95_approx": [round((value - 1.96 * se) * scale, 4), round((value + 1.96 * se) * scale, 4)], "n": n}


def age_standardized(y: pd.DataFrame, sex_code: int, psus: pd.MultiIndex):
    selected = y[y.group.isin(["occupied_no_study", "home_primary"]) & y.P6020.eq(sex_code)].copy()
    std = selected.groupby("age_band", observed=False).FEX_C.sum()
    std = std / std.sum()
    if std.isna().any() or (std <= 0).any():
        raise ValueError(f"Hay celdas edad×grupo vacías: {std.to_dict()}")
    output = {}
    group_influence = {}
    for group in ["occupied_no_study", "home_primary"]:
        output[group] = {}
        group_influence[group] = {}
        for col in ["P1895", "P1905", "P3175", "income_sufficient"]:
            estimate = 0.0
            influence = pd.Series(0.0, index=psus)
            for age_band, std_weight in std.items():
                cell_mask = y.group.eq(group) & y.P6020.eq(sex_code) & y.age_band.eq(age_band)
                cell = ratio_estimate(y, cell_mask, col, psus)
                if cell is None:
                    raise ValueError(f"Celda vacía: {group}/{age_band}/{col}")
                cell_est, cell_u, _ = cell
                estimate += float(std_weight) * cell_est
                influence += float(std_weight) * cell_u
            mult = 100 if col == "income_sufficient" else 1
            output[group][col] = {"estimate": round(estimate * mult, 4)}
            group_influence[group][col] = influence
    contrasts = {}
    for col in ["P1895", "P1905", "P3175", "income_sufficient"]:
        d = output["occupied_no_study"][col]["estimate"] - output["home_primary"][col]["estimate"]
        diff_u = group_influence["occupied_no_study"][col] - group_influence["home_primary"][col]
        raw_se = se_taylor(diff_u)
        mult = 100 if col == "income_sufficient" else 1
        contrasts[col] = {
            "occupied_no_study": output["occupied_no_study"][col]["estimate"],
            "home_primary": output["home_primary"][col]["estimate"],
            "difference_occupied_minus_home": round(d, 4),
            "ci95_approx": [round((d - 1.96 * raw_se * mult), 4), round((d + 1.96 * raw_se * mult), 4)],
            "unit": "percentage_points" if col == "income_sufficient" else "mean_0_10",
        }
    return {
        "sex_label": "sexo al nacer (P6020=2; mujeres)",
        "sample_n": {g: int((selected.group == g).sum()) for g in ["occupied_no_study", "home_primary"]},
        "age_bands": [x[2] for x in AGE_BANDS],
        "standard_reference": {str(k): round(float(v), 8) for k, v in std.items()},
        "estimates": output,
        "contrasts": contrasts,
        "ci_note": "IC aproximados por linealización de Taylor por estrato y segmento; distribución estándar FEX_C fija, condicionada al estándar.",
    }


def main():
    y = load_data()
    psus = design_index(y)
    groups = []
    sex_views = {"all": [], "women": [], "men": []}
    mapping = [("all", None), ("women", 2), ("men", 1)]
    for gid, name in GROUPS:
        m = y.group.eq(gid)
        nf = int((m & y.P6020.eq(2)).sum())
        nm = int((m & y.P6020.eq(1)).sum())
        female_weight = float(y.loc[m & y.P6020.eq(2), "FEX_C"].sum())
        male_weight = float(y.loc[m & y.P6020.eq(1), "FEX_C"].sum())
        both_weight = female_weight + male_weight
        row = {
            "id": gid, "name": name, "sample_n": int(m.sum()),
            "sample_n_women": nf, "sample_n_men": nm,
            "weighted_sex_at_birth_pct": {
                "women_P6020_2": round(100 * female_weight / both_weight, 4),
                "men_P6020_1": round(100 * male_weight / both_weight, 4),
            },
        }
        groups.append(row)
        for view, code in mapping:
            vm = m if code is None else m & y.P6020.eq(code)
            denominator = y.FEX_C.sum() if code is None else y.loc[y.P6020.eq(code), "FEX_C"].sum()
            group_weight = float(y.loc[vm, "FEX_C"].sum())
            n = int(vm.sum())
            outcomes = None
            if n >= 50:
                outcomes = {
                    "life_satisfaction": estimate_json(y, vm, "P1895", psus),
                    "activities_worthwhile": estimate_json(y, vm, "P1905", psus),
                    "free_time_satisfaction": estimate_json(y, vm, "P3175", psus),
                    "household_income_sufficient_pct": estimate_json(y, vm, "income_sufficient", psus, 100),
                }
            sex_views[view].append({
                "id": gid, "name": name, "sample_n": n,
                "weighted_share_pct": round(100 * group_weight / denominator, 4),
                "outcomes": outcomes,
                "below_minimum_n": n < 50,
            })
    sex_composition = {
        "title": "Composición por sexo al nacer dentro de cada configuración",
        "variable": "P6020",
        "label": "sexo al nacer (no identidad de género)",
        "groups": groups,
    }
    sensitivity = age_standardized(y, 2, psus)
    data = {
        "title": "ECV 2025 · jóvenes de 18 a 28 años",
        "source_modules": ["Características y composición del hogar", "Condiciones de vida del hogar y tenencia de bienes", "Educación", "Fuerza de trabajo", "Variables de diseño muestral"],
        "sample_design": {"weight": "FEX_C", "strata": "ESTRATO2020", "primary_sampling_unit": "SEGMENTO", "strata_count": int(y.ESTRATO2020.nunique()), "segment_count": int(y[["ESTRATO2020", "SEGMENTO"]].drop_duplicates().shape[0]), "ci_method": "Linealización de Taylor de primer orden, con estratos y segmentos."},
        "sex_at_birth": sex_composition,
        "minimum_unweighted_n_for_interactive_outcomes": 50,
        "views": sex_views,
        "women_only_age_standardized_sensitivity": sensitivity,
        "classification": {
            "employment": "P6240=1 o Sí en P6250/P6260/P6270.",
            "study": "P8586=1.",
            "home_primary": "Sin estudio ni ocupación derivada y P6240=4.",
            "priority": [g[0] for g in GROUPS],
            "sex": "Sexo al nacer, variable original del DANE P6020; P6020=2 mujeres y P6020=1 hombres. No mide identidad de género.",
        },
        "limitations": ["ECV transversal: no identifica causalidad, decisiones, preferencias ni trayectorias.", "P9090 es suficiencia económica declarada por el hogar, no ingreso individual.", "Las estimaciones de bienestar son medias o proporciones separadas, sin índice ni ranking.", "Los IC son aproximados por linealización y, en la sensibilidad estandarizada, condicionados a la distribución común por edad fijada."],
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "ecv2025_sex.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pd.DataFrame([{
        "id": g["id"], "configuracion": g["name"], "n_muestral": g["sample_n"],
        "n_mujeres": g["sample_n_women"], "n_hombres": g["sample_n_men"],
        "mujeres_sexo_al_nacer_pct_ponderado": g["weighted_sex_at_birth_pct"]["women_P6020_2"],
        "hombres_sexo_al_nacer_pct_ponderado": g["weighted_sex_at_birth_pct"]["men_P6020_1"],
    } for g in groups]).to_csv(OUT / "ecv2025_sex_composition.csv", index=False, encoding="utf-8-sig")
    print("\nComposición por sexo dentro de grupo:")
    for g in groups:
        print(g["id"], g["sample_n"], g["sample_n_women"], g["sample_n_men"], g["weighted_sex_at_birth_pct"])
    print("\nAnálisis restringido a mujeres estandarizado por edad:")
    print(json.dumps(sensitivity, ensure_ascii=False, indent=2))
    assert groups[2]["sample_n"] == 18189 and groups[2]["weighted_sex_at_birth_pct"]["women_P6020_2"] == 39.1815
    assert groups[3]["sample_n"] == 7205 and groups[3]["weighted_sex_at_birth_pct"]["women_P6020_2"] == 90.4126
    assert sensitivity["sample_n"] == {"occupied_no_study": 6877, "home_primary": 6514}


if __name__ == "__main__":
    main()
