#!/usr/bin/env python3
"""Exporta agregados ECV 2025 para el laboratorio; no escribe microdatos."""
import json, sys, zipfile
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "data/fuente_ecv"
KEY = ["DIRECTORIO", "SECUENCIA_P", "ORDEN"]
HKEY = ["DIRECTORIO", "SECUENCIA_P"]


def read(pattern, columns, key):
    files = list(DATA.glob(pattern))
    if len(files) != 1:
        raise FileNotFoundError(f"{pattern}: se esperaba 1 ZIP, hay {len(files)}")
    with zipfile.ZipFile(files[0]) as z:
        csvs = [f for f in z.namelist() if f.lower().endswith(".csv")]
        if len(csvs) != 1:
            raise ValueError(f"{files[0].name}: número de CSV inesperado")
        df = pd.read_csv(z.open(csvs[0]), sep=";", decimal=",", encoding="latin1",
                         usecols=columns, low_memory=False)
    if key is not None and df.duplicated(key).any():
        raise ValueError(f"Claves duplicadas en {files[0].name}")
    return df


def join(left, right, on, validate):
    out = left.merge(right, on=on, how="left", validate=validate, indicator=True)
    if not out["_merge"].eq("both").all() or len(out) != len(left):
        raise ValueError(f"Integración incompleta: {out['_merge'].value_counts().to_dict()}")
    return out.drop(columns="_merge")


def main():
    p = read("*Caracteristicas*2025*.zip", KEY + ["P6040", "P6020", "P1895", "P3175", "P1905"], KEY)
    w = read("*Fuerza_trabajo*2025*.zip", KEY + ["P6240", "P6250", "P6260", "P6270", "P6280"], KEY)
    e = read("*Educacion*2025*.zip", KEY + ["P8586"], KEY)
    d = read("*Variables_diseno_muestral*2025*.zip", KEY + ["SEGMENTO", "ESTRATO2020", "FEX_C"], KEY)
    h = read("*Condiciones_vida_hogar_tenencia_bienes*2025*.zip",
             ["DIRECTORIO", "SECUENCIA_ENCUESTA", "SECUENCIA_P", "ORDEN", "P9090"], None)
    # El módulo de hogar codifica el hogar en ORDEN; validar antes del cambio de llave.
    if not h.ORDEN.eq(h.SECUENCIA_ENCUESTA).all() or not h.SECUENCIA_P.eq(1).all():
        raise ValueError("La llave del módulo de hogar no corresponde a la estructura esperada")
    h = h.drop(columns=["SECUENCIA_P", "SECUENCIA_ENCUESTA"]).rename(columns={"ORDEN": "SECUENCIA_P"})
    if set(map(tuple, p[HKEY].drop_duplicates().to_numpy())) != set(map(tuple, h[HKEY].to_numpy())):
        raise ValueError("No coincide la cobertura de hogares")

    y = p[p.P6040.between(18, 28)].copy()
    n = len(y)
    for frame, key, cardinality in [(w, KEY, "one_to_one"), (e, KEY, "one_to_one"),
                                    (d, KEY, "one_to_one"), (h, HKEY, "many_to_one")]:
        y = join(y, frame, key, cardinality)
    required = ["P8586", "P6240", "P1895", "P3175", "P1905", "P9090", "FEX_C"]
    if y[required].isna().any().any() or not y.FEX_C.gt(0).all() or not y.P9090.isin([1, 2, 3]).all():
        raise ValueError("Faltan resultados, ponderadores positivos o códigos esperados")
    for col in ["P1895", "P3175", "P1905"]:
        if not y[col].between(0, 10).all():
            raise ValueError(f"{col} fuera de escala")

    employed = y.P6240.eq(1) | y[["P6250", "P6260", "P6270"]].eq(1).any(axis=1)
    studying = y.P8586.eq(1)
    home = ~employed & ~studying & y.P6240.eq(4)
    search = ~employed & ~studying & ~home & y.P6280.eq(1)
    ids = ["occupied_no_study", "study_no_occupation", "study_and_work",
           "home_primary", "searched_elsewhere", "other"]
    y["configuration"] = np.select(
        [employed & ~studying, studying & ~employed, studying & employed, home, search], ids[:-1], default="other"
    )
    y["income_minimum"] = y.P9090.ge(2)
    weight_total = float(y.FEX_C.sum())
    psus = d[["ESTRATO2020", "SEGMENTO"]].drop_duplicates()
    psu_index = pd.MultiIndex.from_frame(psus)

    def estimate(mask, values):
        a = y.loc[mask, ["ESTRATO2020", "SEGMENTO", "FEX_C"]].copy()
        a["x"] = values.loc[mask].to_numpy()
        den = float(a.FEX_C.sum())
        if den <= 0:
            raise ValueError("Dominio vacío")
        mean = float((a.FEX_C * a.x).sum() / den)
        a["u"] = a.FEX_C * (a.x - mean) / den
        u = a.groupby(["ESTRATO2020", "SEGMENTO"]).u.sum().reindex(psu_index, fill_value=0.0)
        return mean, u, len(a)

    def se(u):
        v = u.groupby(level=0).agg(["count", "var"])
        return float(np.sqrt(max(0, (v["count"] * v["var"].fillna(0)).sum())))

    names = [
        ("occupied_no_study", "Ocupados que no estudian", "Ocupación derivada; P8586=No."),
        ("study_no_occupation", "Estudiantes sin ocupación", "P8586=Sí; sin ocupación derivada."),
        ("study_and_work", "Estudian y trabajan", "P8586=Sí y ocupación derivada."),
        ("home_primary", "Oficios del hogar como actividad principal", "P6240=oficios del hogar; no estudia ni está ocupada."),
        ("searched_elsewhere", "Búsqueda reciente de empleo (resto)", "P6280=Sí entre categorías no asignadas antes."),
        ("other", "Otras situaciones", "Resto de situaciones sin estudio ni ocupación derivada."),
    ]
    groups = []
    for gid, label, definition in names:
        mask = y.configuration.eq(gid)
        outcomes = {}
        for var, outkey, scale in [("P1895", "life_satisfaction", 1),
                                   ("P1905", "activities_worthwhile", 1),
                                   ("P3175", "free_time_satisfaction", 1),
                                   ("income_minimum", "household_income_reaches_minimum", 100)]:
            values = y[var].astype(float) if var == "income_minimum" else y[var]
            m, u, dn = estimate(mask, values)
            if dn != int(mask.sum()):
                raise ValueError(f"Denominador desigual: {gid}/{outkey}")
            margin = 1.96 * se(u)
            outcomes[outkey] = {"estimate": round(m * scale, 3),
                                "ci95_approx": [round((m-margin)*scale, 3), round((m+margin)*scale, 3)],
                                "unit": "percent" if scale == 100 else "mean_0_10"}
        groups.append({"id": gid, "name": label, "definition": definition,
                       "sample_n": int(mask.sum()),
                       "weighted_share_pct": round(100 * float(y.loc[mask, "FEX_C"].sum()) / weight_total, 2),
                       "outcomes": outcomes})
    if sum(g["sample_n"] for g in groups) != n:
        raise ValueError("Las seis configuraciones no cubren todos los registros")

    y["age_band"] = pd.cut(y.P6040, [17, 21, 25, 28], labels=False)
    y["cell"] = y.P6020.astype(str) + "_" + y.age_band.astype(str)
    pair = y.configuration.isin(["home_primary", "occupied_no_study"])
    standard = y.loc[pair].groupby("cell").FEX_C.sum()
    standard = standard / standard.sum()

    def standardized(gid, values):
        estimates = [estimate(y.configuration.eq(gid) & y.cell.eq(c), values) for c in standard.index]
        if min(x[2] for x in estimates) == 0:
            raise ValueError(f"Falta soporte común para {gid}")
        m = float(sum(a*x[0] for a,x in zip(standard, estimates)))
        u = sum((a*x[1] for a,x in zip(standard, estimates)))
        return m, u

    contrasts = {}
    for var, key, scale in [("P1895", "life_satisfaction", 1),
                             ("P1905", "activities_worthwhile", 1),
                             ("P3175", "free_time_satisfaction", 1),
                             ("income_minimum", "household_income_reaches_minimum", 100)]:
        values = y[var].astype(float) if var == "income_minimum" else y[var]
        hm, hu = standardized("home_primary", values)
        wm, wu = standardized("occupied_no_study", values)
        delta, margin = hm-wm, 1.96*se(hu-wu)
        contrasts[key] = {"home_primary": round(hm*scale, 3), "occupied_no_study": round(wm*scale, 3),
                          "difference_home_minus_work": round(delta*scale, 3),
                          "ci95_approx": [round((delta-margin)*scale, 3), round((delta+margin)*scale, 3)],
                          "unit": "percentage_points" if scale == 100 else "mean_0_10"}
    thresholds = []
    for t in [7, 8, 9]:
        joint = y[["P1895", "P1905", "P3175"]].ge(t).all(axis=1) & y.income_minimum
        hm, hu = standardized("home_primary", joint.astype(float))
        wm, wu = standardized("occupied_no_study", joint.astype(float))
        delta, margin = hm-wm, 1.96*se(hu-wu)
        thresholds.append({"threshold": t, "home_primary_pct": round(hm*100, 3),
                           "occupied_no_study_pct": round(wm*100, 3),
                           "difference_home_minus_work_pp": round(delta*100, 3),
                           "ci95_approx_pp": [round((delta-margin)*100, 3), round((delta+margin)*100, 3)]})

    out = {
        "title": "ECV 2025 · Jóvenes de 18 a 28 años",
        "source": {"agency": "DANE", "catalog": "https://microdatos.dane.gov.co/index.php/catalog/905",
                   "dictionary": "https://microdatos.dane.gov.co/index.php/catalog/905/data-dictionary"},
        "population_age": [18, 28], "person_records": int(len(y)),
        "households": int(y[HKEY].drop_duplicates().shape[0]), "modules_integrated": 5,
        "records_lost": 0, "weighted_population_sum": round(weight_total, 3), "weight": "FEX_C",
        "design": {"strata": "ESTRATO2020", "primary_sampling_unit": "SEGMENTO",
                   "strata_count": int(psus.ESTRATO2020.nunique()), "segment_count": int(len(psus)),
                   "singleton_strata": int(psus.groupby("ESTRATO2020").size().eq(1).sum()),
                   "interval_note": "IC95% aproximados por linealización de primer orden dentro de estratos; en el contraste, estándar sexo×edad fijo."},
        "standardization": {"variables": "sexo al nacer × edad", "age_bands": ["18–21", "22–25", "26–28"],
                            "reference": "Distribución FEX_C agrupada de ambos grupos (hogar y ocupación sin estudio).",
                            "comparison": "Oficios del hogar menos ocupados que no estudian"},
        "category_rule": {
            "employment": "P6240=1 o Sí en P6250/P6260/P6270.",
            "study": "P8586=1.", "home": "Sin ocupación/estudio y P6240=4.",
            "job_search": "Sin asignación anterior y P6280=1 (diligencia en últimas 4 semanas).",
            "priority": [x[1] for x in names],
            "caveat": "Clasificación analítica excluyente; pueden coexistir actividades. Oficios del hogar sigue la actividad principal y puede incluir búsqueda simultánea. No identifica decisiones ni todo el cuidado no remunerado."
        },
        "groups": groups, "standardized_contrasts": contrasts, "joint_threshold_sensitivity": thresholds,
        "limitations": ["Datos transversales: no identifican causalidad, decisiones o renuncias.",
                       "P9090 es una respuesta del hogar, no ingreso individual.",
                       "IC aproximados y condicionados al estándar común; resultados exploratorios, sin validación de escala ni equivalencia."]
    }
    (ROOT / "data/ecv2025_summary.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pd.DataFrame([{"id":g["id"], "configuracion":g["name"], "n_muestral":g["sample_n"],
                   "porcentaje_ponderado_18_28":g["weighted_share_pct"],
                   "satisfaccion_vital_media_0_10":g["outcomes"]["life_satisfaction"]["estimate"],
                   "sentido_actividad_media_0_10":g["outcomes"]["activities_worthwhile"]["estimate"],
                   "satisfaccion_tiempo_libre_media_0_10":g["outcomes"]["free_time_satisfaction"]["estimate"],
                   "ingresos_hogar_alcanzan_gastos_minimos_pct":g["outcomes"]["household_income_reaches_minimum"]["estimate"]}
                  for g in groups]).to_csv(ROOT / "data/ecv2025_groups.csv", index=False, encoding="utf-8-sig")
    print(f"Exportados solo agregados: n={len(y):,}; hogares={out['households']:,}; grupos={len(groups)}; pérdidas=0")


if __name__ == "__main__":
    main()
