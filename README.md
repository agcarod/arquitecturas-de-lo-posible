# Arquitecturas de lo posible

**Juventudes y condiciones sociales del bienestar en un mundo en transición**  
Ángela Gissette Caro-Delgado, Ph. D.

Laboratorio digital académico preparado para la postulación posdoctoral «Futuros de las Ciencias Sociales» de la Universidad de los Andes.

**Sitio público:** https://agcarod.github.io/arquitecturas-de-lo-posible/  
**Fuentes y metodología:** https://agcarod.github.io/arquitecturas-de-lo-posible/metodologia.html  
**Repositorio:** https://github.com/agcarod/arquitecturas-de-lo-posible

Es una iniciativa académica independiente, no un proyecto institucional aprobado ni una publicación oficial de la Universidad.

## Una pregunta que parte de un hallazgo

En el análisis preliminar de cinco módulos de la ECV 2025 se integraron 35.776 jóvenes de 18–28 años en 27.632 hogares, sin pérdida de registros. La satisfacción vital media fue 8,28/10 entre quienes trabajaban sin estudiar y 8,18 entre quienes realizaban principalmente oficios del hogar, sin estudiar ni estar ocupados. Sin embargo, la proporción de hogares que percibían ingresos suficientes para cubrir al menos sus gastos mínimos fue 69,6 % y 53,1 %, respectivamente: una brecha estandarizada de 16,5 puntos porcentuales (IC 95 % aproximado: 12,1–20,8).

El contraste no demuestra equivalencia ni causalidad. Tampoco revela qué otras vidas podrían elegirse, qué sostiene sus posibilidades o qué habría que cambiar para transformarlas. El laboratorio abre esas preguntas sin reducir el bienestar a un índice.

## Cinco secciones

1. **¿Dónde comienzan nuestras posibilidades?** Atlas de Bogotá D. C., Chocó, La Guajira y Vaupés como contexto territorial. Los denominadores son distintos y no describen la muestra de 18–28 años.
2. **¿Cómo vivimos actualmente?** Seis configuraciones observables de jóvenes en la ECV 2025, con estimaciones ponderadas, frecuencias muestrales y composición por sexo al nacer (P6020).
3. **¿A qué renunciamos para sostener nuestras vidas?** Contrastes estandarizados, intervalos aproximados, sensibilidad a umbrales de 7, 8 y 9 y un análisis restringido a mujeres. La ECV transversal no identifica renuncias ni decisiones.
4. **¿Cómo reconstruir las arquitecturas de lo posible?** Distinciones entre configuración, bienestar, posibilidad y arquitectura; demostración hipotética; antecedentes y evaluación comparativa en el piloto del año 1.
5. **¿Qué sociedades podríamos construir?** Agenda 2027–2030 y líneas posteriores, condicionadas por aprobación ética, renovaciones y recursos.

## Diseño de investigación

En el año 1 se propone ampliar el análisis ECV, replicar contrastes preespecificados en otra edición comparable y complementar con la Encuesta Nacional de Uso del Tiempo, sin vincular registros individuales. Con aval ético y recursos, un piloto con 6–8 jóvenes de Bogotá incluiría dos encuentros separados por seis a ocho semanas. Se reconstruirían hasta dos alternativas prioritarias por persona y se formularían juicios prospectivos sobre accesibilidad y sostenimiento. Dos análisis independientes del material inicial compararían un protocolo de capacidades previamente especificado con el mismo protocolo complementado por una matriz de dependencias, compatibilidad y sostenimiento. El piloto evalúa factibilidad y fuentes de error; no demuestra superioridad generalizable.

El año 2 seguiría aproximadamente a 24 jóvenes nuevos de Bogotá durante ocho meses, con tres encuentros. El año 3 integraría resultados y examinaría ámbitos institucionales para formular hipótesis de transformación, factibilidad y equidad. La ética y los recursos condicionan las fases con participantes.

## Datos y código

Los microdatos del DANE no se publican en este repositorio. El [catálogo oficial de la ECV 2025](https://microdatos.dane.gov.co/index.php/catalog/905) reúne microdatos anonimizados y documentación técnica.

- [CSV agregado por configuración](data/ecv2025_groups.csv)
- [Resumen JSON con estimaciones y método](data/ecv2025_summary.json)
- [Vistas de población total, mujeres y hombres](data/ecv2025_sex.json)
- [Composición por sexo al nacer y tamaños muestrales](data/ecv2025_sex_composition.csv)
- [Generar agregados desde los microdatos descargados](scripts/build_ecv2025_dashboard.py)
- [Generar vistas y composición por sexo](scripts/build_ecv2025_sex_dashboard.py)
- [Código de contraste por sexo](scripts/ECV2025_contraste_por_sexo.py)
- [Scripts de piloto y robustez](scripts/)
- [Trazabilidad científica completa](docs/FUENTES_Y_METODO.md)

Para regenerar los agregados con Python, pandas y numpy:

```bash
python scripts/build_ecv2025_dashboard.py /ruta/a/los/zip-dane
python scripts/build_ecv2025_sex_dashboard.py /ruta/a/los/zip-dane
python scripts/ECV2025_contraste_por_sexo.py /ruta/a/los/zip-dane
```

Los programas validan llaves, cardinalidad, cobertura, composición por sexo y tamaños muestrales. Escriben únicamente archivos agregados; no exportan microdatos individuales. P6020 es sexo al nacer según el DANE, no identidad de género. Las vistas del selector son descriptivas y ponderadas; la sensibilidad de mujeres se estandariza por edad.

## Alcance científico

La propuesta conversa con capacidades, factores de conversión, tiempo e ingresos, aspiraciones, curso de vida, seguridad de oportunidades y experiencia psicosocial del empleo. La contribución potencial es desarrollar y evaluar un procedimiento que conecte alternativas de vida valoradas con restricciones y apoyos documentados, compatibilidad, sostenimiento y experiencia psicológica. La validez, la utilidad adicional y la transferibilidad siguen por establecerse; no se reclama novedad absoluta ni superioridad anticipada. La búsqueda bibliográfica es focalizada, no una revisión sistemática.

El recurso C/R/U es una demostración metodológica hipotética, no una escala validada ni un modelo predictivo. Las cifras territoriales son contextuales y de unidades diferentes. Los datos ECV son transversales y no causales.

## Reproducir

```bash
node --check app.js
node --test tests/data.test.cjs
```

## Licencia

El código del prototipo se distribuye bajo la licencia MIT incluida en [LICENSE](LICENSE). El uso de los datos de terceros sigue las condiciones definidas por el DANE.
