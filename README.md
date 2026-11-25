# Arquitecturas de lo posible

**Juventudes y condiciones sociales del bienestar en un mundo en transición**  
Autora: Ángela Gissette Caro-Delgado, Ph. D.

Laboratorio digital académico para la propuesta posdoctoral «Futuros de las Ciencias Sociales» de la Universidad de los Andes. Reúne un atlas territorial, análisis agregado del piloto ECV 2025, contrastes exploratorios, una demostración metodológica y una agenda de investigación.

- **Sitio público:** https://agcarod.github.io/arquitecturas-de-lo-posible/
- **Fuentes, métodos y resultados:** https://agcarod.github.io/arquitecturas-de-lo-posible/metodologia.html
- **Repositorio:** https://github.com/agcarod/arquitecturas-de-lo-posible

Es una iniciativa académica independiente; no constituye un proyecto institucional aprobado ni una publicación oficial de la Universidad de los Andes.

## Cinco preguntas del laboratorio

1. **¿Dónde comienzan nuestras posibilidades?** Atlas de Bogotá D. C., Chocó, La Guajira y Vaupés; conserva denominadores y límites de indicadores, y la serie FIES 2023–2025.
2. **¿Cómo vivimos actualmente?** Cinco módulos ECV 2025 enlazados para 35.776 personas de 18–28 años en 27.632 hogares, sin pérdidas; seis configuraciones y estimaciones ponderadas.
3. **¿A qué renunciamos para sostener nuestras vidas?** Contraste de oficios del hogar y ocupación sin estudio, estandarizado por sexo y edad, con intervalos aproximados y sensibilidad al umbral.
4. **¿Cómo reconstruir las arquitecturas de lo posible?** Cuatro distinciones analíticas, demostración interactiva hipotética, antecedentes y un plan para evaluar valor añadido frente a un comparador fuerte.
5. **¿Qué sociedades podríamos construir?** Agenda posdoctoral 2027–2030 condicionada por ética, renovaciones y financiación; productos académicos y líneas posteriores.

## Resultados principales

- Las valoraciones agregadas se presentan por separado: satisfacción vital, P1905 (qué tanto las cosas que se hacen valen la pena), satisfacción con tiempo libre y suficiencia económica percibida del hogar.
- Oficios del hogar y ocupación sin estudio muestran valoraciones medias relativamente próximas en unos resultados y diferentes en otros; el grupo de oficios del hogar informa menor suficiencia económica del hogar y mayor satisfacción con el tiempo libre.
- El porcentaje que supera el indicador conjunto depende del corte: al usar ≥7, ≥8 y ≥9 cambia la diferencia entre grupos; al corte ≥9 el IC aproximado incluye cero. Esto no demuestra equivalencia.
- Los datos transversales no identifican renuncias, decisiones, libertad efectiva o causalidad. El resultado empírico abre preguntas y no prueba la hipótesis institucional.

## Datos y código

Los microdatos DANE no se publican en este repositorio. El portal del DANE incluye el [catálogo, documentación y diccionario de la ECV 2025](https://microdatos.dane.gov.co/index.php/catalog/905).

- [CSV agregado por configuración](data/ecv2025_groups.csv)
- [Resumen JSON con método y estimaciones](data/ecv2025_summary.json)
- [Generar ambos desde los microdatos descargados](scripts/build_ecv2025_dashboard.py)
- [Scripts de piloto y robustez](scripts/)
- [Prueba de reglas C/R/U](scripts/prueba_logica_arquitecturas.py)
- [Trazabilidad científica completa](docs/FUENTES_Y_METODO.md)

Para regenerar los agregados con Python, pandas y numpy:

```bash
python scripts/build_ecv2025_dashboard.py /ruta/a/los/zip-dane
```

El programa valida unicidad, cardinalidad, cobertura y valores esperados. Escribe solo el resumen JSON y el CSV agregado; no exporta microdatos.

## Alcance científico

La capacidad, los factores de conversión, el tiempo e ingreso, las aspiraciones, el curso de vida, la experiencia psicológica del empleo y la seguridad de oportunidades tienen antecedentes. La posible aportación es desarrollar y contrastar un procedimiento que conecte alternativas de vida valoradas, requisitos documentados, compatibilidad, dependencia y experiencia psicológica. Su validez, utilidad adicional, confiabilidad, transferibilidad y superioridad siguen sin demostrarse. La búsqueda bibliográfica usada hasta ahora es focalizada, no una revisión sistemática.

Las cifras territoriales son agregadas y no tienen una unidad común. El resumen ECV es transversal, no causal. El prototipo interactivo no predice trayectorias ni es una escala validada. La metodología de campo y cualquier recopilación con personas dependen de la aprobación ética y los recursos.

## Reproducir y verificar

```bash
node --check app.js
node --test tests/data.test.cjs
python scripts/prueba_logica_arquitecturas.py
```

## Licencia y atribución

El código del prototipo se distribuye bajo la licencia MIT incluida en [LICENSE](LICENSE). El uso de datos de terceros sigue las condiciones definidas por DANE. El proyecto no representa posiciones institucionales del DANE, la Universidad de los Andes ni otras entidades.
