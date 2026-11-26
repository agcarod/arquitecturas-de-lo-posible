# Fuentes, método y resultados

La ficha pública completa se encuentra en [metodologia.html](../metodologia.html) y puede leerse también en el [sitio publicado](https://agcarod.github.io/arquitecturas-de-lo-posible/metodologia.html).

## Estado de evidencia

- El atlas territorial conserva tres indicadores DANE como contexto agregado; sus unidades y grupos de edad difieren. No representa la muestra ECV de 18–28 años. Se retiraron las estimaciones secundarias de población 0–17.
- El piloto enlazó cinco módulos ECV 2025 para 35.776 personas de 18–28 años, distribuidas en 27.632 hogares, sin pérdida de registros.
- El resumen público contiene estimaciones ponderadas con FEX_C, frecuencias muestrales sin ponderar y contrastes estandarizados con intervalos aproximados.
- Se añadieron composición ponderada por sexo al nacer (P6020) para las seis configuraciones, vistas descriptivas para población total/mujeres/hombres y sensibilidad estandarizada por edad dentro de mujeres. P6020 no mide identidad de género.
- En ocupados sin estudiar (n=18.189), las mujeres representan 39,2 % y los hombres 60,8 %; en oficios del hogar (n=7.205), las mujeres representan 90,4 % y los hombres 9,6 %.
- La sensibilidad restringida a mujeres incluye 6.877 ocupadas sin estudiar y 6.514 en oficios del hogar. La diferencia ponderada y estandarizada por edad en suficiencia económica percibida del hogar es 17,24 p. p. (IC 95 % aproximado: 14,24–20,25); la satisfacción vital difiere en 0,20 puntos (0,10–0,30).
- Los contrastes son exploratorios y transversales. No identifican renuncias, decisiones, libertad efectiva ni causalidad; el indicador conjunto es sensible al umbral.
- El piloto metodológico propuesto para el año 1 contempla 6–8 jóvenes y dos encuentros separados por seis a ocho semanas; la comparación de dos análisis y los juicios prospectivos se realizarían en esta fase, con aprobación ética y recursos.

## Reproducción

Los microdatos no se incluyen en este repositorio. Descárgalos del [catálogo ECV 2025 del DANE](https://microdatos.dane.gov.co/index.php/catalog/905/get_microdata), instala pandas y numpy y ejecuta:

```bash
python scripts/build_ecv2025_dashboard.py /ruta/a/los/zip-dane
python scripts/build_ecv2025_sex_dashboard.py /ruta/a/los/zip-dane
python scripts/ECV2025_contraste_por_sexo.py /ruta/a/los/zip-dane
```

El script valida las integraciones y genera solo agregados. Los archivos de resultados, fuentes y límites de inferencia se documentan en [la ficha](../metodologia.html#ecv).

## Código y datos agregados

- [CSV por configuraciones](../data/ecv2025_groups.csv)
- [Resumen JSON con estimaciones y método](../data/ecv2025_summary.json)
- [Vistas por sexo en JSON](../data/ecv2025_sex.json)
- [Composición por sexo en CSV](../data/ecv2025_sex_composition.csv)
- [Código para regenerar los agregados](../scripts/build_ecv2025_dashboard.py)
- [Generador por sexo](../scripts/build_ecv2025_sex_dashboard.py)
- [Código de contraste por sexo](../scripts/ECV2025_contraste_por_sexo.py)
- [Salida del análisis de robustez](../results/resultado_robustez_ecv.txt)
- [Salida reproducida de composición y contraste](../results/resultado_contraste_por_sexo.txt)
