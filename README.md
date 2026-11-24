# ¿Cuántas puertas se abren donde creces?

**Futuros en prueba · Arquitecturas de lo posible**  
Prototipo interactivo para explorar desigualdades en condiciones territoriales de acceso y privación en Colombia. La comparación es descriptiva: no mide trayectorias individuales ni determina posibilidades de vida. Preparado como demostración académica de una agenda de investigación interdisciplinaria.


**Propuesta académica de Ángela Gissette Caro-Delgado, Ph.D.**  
Demostración preparada para la **postulación a la convocatoria posdoctoral «Futuros de las Ciencias Sociales» de la Facultad de Ciencias Sociales de la Universidad de los Andes (2026)**. Es una iniciativa independiente, no un proyecto institucional aprobado por la Universidad.

![Estado](https://img.shields.io/badge/estado-prototipo_académico-246f69?style=flat-square) ![Tecnologías](https://img.shields.io/badge/tecnologías-HTML%20%2B%20CSS%20%2B%20JS-728e82?style=flat-square)

> **Pregunta:** ¿Cómo se distribuyen algunas condiciones materiales, educativas y digitales en cuatro territorios, y qué queda fuera cuando se leen como promedios?

## ¿Qué incluye?

- **Cuatro territorios** para explorar: Chocó, La Guajira, Bogotá D. C. y Vaupés.
- **Población 0–17 años** y desglose 0–11 / 12–17 (tabulaciones secundarias de proyecciones DANE 2025).
- **Tres indicadores publicados por DANE para 2025**: hogares con acceso a internet; hogares con inseguridad alimentaria moderada o grave; asistencia a educación formal de jóvenes **17–21** (una transición posterior, no medida del total 0–17).
- **Serie 2023–2025** de inseguridad alimentaria, con variaciones 2024–2025 significativas documentadas por DANE en los cuatro casos.
- **Generador de preguntas exploratorias** sobre lo que los agregados no responden. Sus diseños son ejemplos metodológicos, no el protocolo empírico de la propuesta posdoctoral.
- **Capa pendiente de violencia y protección**, con enlace a RUV pero sin atribuir una cifra no verificada.
- Metodología, referencias, CSV descargable y archivos fuente editables.

**Aviso científico:** los indicadores poseen **denominadores distintos**. No se suman, no se ponderan en un índice y no estiman riesgo individual ni prueban causalidad. Describen condiciones agregadas; no miden futuros deseados, posibilidades percibidas, opciones reales ni bienestar.

## Publicación verificada

- **Web:** https://agcarod.github.io/arquitecturas-de-lo-posible/
- **Repositorio:** https://github.com/agcarod/arquitecturas-de-lo-posible
- **Ficha metodológica legible:** https://agcarod.github.io/arquitecturas-de-lo-posible/metodologia.html

## Probar antes de subir

Abre `index.html` directamente en tu navegador. También puedes servirlo localmente:

```bash
python3 -m http.server 8000
```

Después visita `http://localhost:8000`.

Verificar sintaxis JavaScript y consistencia interna:

```bash
node --check app.js
node --test tests/data.test.cjs
```

## Estructura del proyecto

```text
index.html                         Página del sitio
styles.css                         Estilos y diseño responsivo
app.js                             Interacciones y gráficos
assets/favicon.svg                 Símbolo del sitio
data/territorios.js                Datos integrados y enlaces
 data/indicadores_2025.csv         Datos tabulares reutilizables
 metodologia.html          Trazabilidad científica y limitaciones
 tests/data.test.cjs               Pruebas automáticas sin dependencias
 .nojekyll                         Publicación directa con GitHub Pages
 LICENSE                           Licencia del código
```

## Alcance y ética

Es un **prototipo académico**, no una plataforma de vigilancia clínica, una herramienta de focalización de menores o un diagnóstico territorial. Las cifras son agregadas. No almacena datos personales, no rastrea visitantes y no envía información a servidores. La herramienta que formula preguntas **no identifica efectos de intervenciones**.

Los valores demográficos de esta versión proceden de tabulaciones secundarias de proyecciones DANE 2025 reproducidas por Telencuestas. La integración de la tabla original del DANE/ICBF y de estimaciones de precisión está identificada como un siguiente paso en la ficha metodológica. No mezclar series de población de distintas revisiones sin documentar el cambio de versión.

## Relación con la propuesta posdoctoral

El tablero conserva una primera capa de contexto territorial. La propuesta posdoctoral, en cambio, estudiaría transiciones entre educación y trabajo con jóvenes de 18–28 años en Bogotá. El tablero no es la muestra del estudio ni mide las trayectorias de sus participantes. La investigación propuesta contrastaría logros con futuros deseados, posibilidades percibidas y opciones documentables —acceso, costos, apoyos, seguridad y tiempo—, además de las experiencias de autonomía, competencia, vínculos, sentido y contribución. Estas categorías serían exploratorias, no un índice ni una definición universal de bienestar.

### Atribución

Datos: Departamento Administrativo Nacional de Estadística (DANE); proyecciones basadas en CNPV 2018; consultas de RUV de la Unidad para las Víctimas como fuente futura. Véase [FUENTES_Y_METODO.md](metodologia.html) para las páginas exactas y los enlaces. El prototipo no representa posiciones institucionales del DANE, la Universidad de los Andes ni la Unidad para las Víctimas.

## Licencia

Código del prototipo: MIT, incluido en [LICENSE](LICENSE). La licencia del código no altera las condiciones de reutilización de las fuentes de datos de terceros.

**Preservación:** la integración Zenodo no está completada; no existe DOI atribuido a esta versión hasta que el depósito sea publicado.