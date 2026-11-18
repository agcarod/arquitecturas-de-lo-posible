# ¿Cuántas puertas se abren donde creces?

**Futuros en prueba · Arquitecturas de lo posible**  
Prototipo interactivo para explorar condiciones territoriales de oportunidad y adversidad en Colombia. Preparado como demostración académica de una agenda de investigación interdisciplinaria.


**Propuesta académica de Ángela Gissette Caro-Delgado, Ph.D.**  
Demostración preparada para la **postulación a la convocatoria posdoctoral «Futuros de las Ciencias Sociales» de la Facultad de Ciencias Sociales de la Universidad de los Andes (2026)**. Es una iniciativa independiente, no un proyecto institucional aprobado por la Universidad.

![Estado](https://img.shields.io/badge/estado-prototipo_académico-246f69?style=flat-square) ![Tecnologías](https://img.shields.io/badge/tecnologías-HTML%20%2B%20CSS%20%2B%20JS-728e82?style=flat-square)

> **Pregunta:** ¿Cómo varían las condiciones materiales, educativas y digitales que rodean las trayectorias de niñas, niños y adolescentes según el territorio donde crecen?

## ¿Qué incluye?

- **Cuatro territorios** para explorar: Chocó, La Guajira, Bogotá D. C. y Vaupés.
- **Población 0–17 años** y desglose 0–11 / 12–17 (tabulaciones secundarias de proyecciones DANE 2025).
- **Tres indicadores publicados por DANE para 2025**: hogares con acceso a internet; hogares con inseguridad alimentaria moderada o grave; asistencia a educación formal de jóvenes **17–21** (una transición posterior, no medida del total 0–17).
- **Cambios 2024–2025** de inseguridad alimentaria, con resultados significativos documentados por DANE para los cuatro territorios.
- **Generador de preguntas y diseños de investigación** para dar el paso de la descripción al contraste de mecanismos e hipótesis.
- **Capa pendiente de violencia y protección**, con enlace a RUV pero sin atribuir una cifra no verificada.
- Metodología, referencias, CSV descargable y archivos fuente editables.

**Aviso científico:** los indicadores poseen **denominadores distintos**. No se suman, no se ponderan en un índice, no estiman riesgo individual ni prueban causalidad.

## Publicar en GitHub Pages — sin instalar nada

1. Inicia sesión en [GitHub](https://github.com/) y selecciona **New repository**.
2. Crea un repositorio, por ejemplo `cuantas-puertas-se-abren`, con visibilidad **Public** si quieres que los jurados accedan sin autenticación.
3. Sube **los archivos y carpetas que aparecen en este ZIP** a la **raíz del repositorio**. Debe existir `index.html` directamente en la raíz, no dentro de otra carpeta.
4. Abre **Settings → Pages**, selecciona **Deploy from a branch**, rama `main` y carpeta `/ (root)`, y guarda la configuración.
5. Una vez publicado, abre la URL que GitHub muestre en **Pages**. Habitualmente será `https://agcarod.github.io/arquitecturas-de-lo-posible/`, pero usa la URL exacta confirmada por GitHub.
6. Prueba en una ventana privada que el enlace abre sin iniciar sesión. Ese será el enlace que podrás insertar en la carta.

> No incluye ni requiere cuenta de GitHub, tokens, bases de datos privadas, paquetes npm, claves ni servicios de terceros. Todo el sitio funciona con archivos estáticos y **rutas relativas**, por lo que sirve tanto en la raíz de un dominio como en un subdirectorio de GitHub Pages.

### Publicar mediante git (alternativa)

```bash
unzip Puertas_Abiertas_Colombia_GitHub.zip
cd Puertas_Abiertas_Colombia_GitHub
git init
git add .
git commit -m "Publicar prototipo: Cuántas puertas se abren"
git branch -M main
git remote add origin https://github.com/agcarod/arquitecturas-de-lo-posible.git
git push -u origin main
```

Repositorio público de la autora: https://github.com/agcarod/arquitecturas-de-lo-posible .

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
 docs/FUENTES_Y_METODO.md          Trazabilidad científica y limitaciones
 tests/data.test.cjs               Pruebas automáticas sin dependencias
 .nojekyll                         Publicación directa con GitHub Pages
 LICENSE                           Licencia del código
```

## Alcance y ética

Es un **prototipo académico**, no una plataforma de vigilancia clínica, una herramienta de focalización de menores o un diagnóstico territorial. Las cifras son agregadas. No almacena datos personales, no rastrea visitantes y no envía información a servidores. La herramienta que formula preguntas **no identifica efectos de intervenciones**.

Los valores demográficos de esta versión proceden de tabulaciones secundarias de proyecciones DANE 2025 reproducidas por Telencuestas. La integración de la tabla original del DANE/ICBF y de estimaciones de precisión está identificada como un siguiente paso en la ficha metodológica. No mezclar series de población de distintas revisiones sin documentar el cambio de versión.

### Atribución

Datos: Departamento Administrativo Nacional de Estadística (DANE); proyecciones basadas en CNPV 2018; consultas de RUV de la Unidad para las Víctimas como fuente futura. Véase [FUENTES_Y_METODO.md](docs/FUENTES_Y_METODO.md) para las páginas exactas y los enlaces. El prototipo no representa posiciones institucionales del DANE, la Universidad de los Andes ni la Unidad para las Víctimas.

## Licencia

Código del prototipo: MIT, incluido en [LICENSE](LICENSE). La licencia del código no altera las condiciones de reutilización de las fuentes de datos de terceros.