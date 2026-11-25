# Fuentes, método y resultados

La ficha pública completa se encuentra en [metodologia.html](../metodologia.html) y puede leerse también en el [sitio publicado](https://agcarod.github.io/arquitecturas-de-lo-posible/metodologia.html).

## Estado de evidencia

- El atlas territorial conserva indicadores del DANE para 2025; las series tienen universos distintos y los recuentos de población 0–17 proceden de una compilación secundaria atribuida a proyecciones DANE que no se ha cotejado con el anexo oficial vigente.
- El piloto enlazó cinco módulos ECV 2025 para 35.776 personas de 18–28 años, distribuidas en 27.632 hogares, sin pérdida de registros.
- El resumen público contiene estimaciones ponderadas con FEX_C, frecuencias muestrales sin ponderar y contrastes estandarizados con intervalos aproximados.
- Los contrastes son exploratorios y transversales. No identifican renuncias, decisiones, libertad efectiva ni causalidad; el indicador conjunto es sensible al umbral.
- La propuesta metodológica está en desarrollo. Diez casos sintéticos y 27 combinaciones lógicas prueban consistencia interna, no validez ni superioridad.

## Reproducción

Los microdatos no se incluyen en este repositorio. Descárgalos del [catálogo ECV 2025 del DANE](https://microdatos.dane.gov.co/index.php/catalog/905/get_microdata), instala pandas y numpy y ejecuta:

```bash
python scripts/build_ecv2025_dashboard.py /ruta/a/los/zip-dane
```

El script valida las integraciones y genera solo agregados. Los archivos de resultados, fuentes y límites de inferencia se documentan en [la ficha](../metodologia.html#ecv).

## Código y datos agregados

- [CSV por configuraciones](../data/ecv2025_groups.csv)
- [Resumen JSON con estimaciones y método](../data/ecv2025_summary.json)
- [Código para regenerar los agregados](../scripts/build_ecv2025_dashboard.py)
- [Salida del análisis de robustez](../results/resultado_robustez_ecv.txt)
- [Salida de prueba lógica](../results/resultado_prueba_logica.txt)
