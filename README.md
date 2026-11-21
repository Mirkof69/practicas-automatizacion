# Prácticas de automatización de pruebas

Materia **Testing, Quality Assurance** · Universidad Privada Franz Tamayo · Docente: Reynel Sánchez Chuquimia ·
Estudiante: Miguel Mirkof Becerra Guzmán

Tres prácticas sobre el sitio de práctica [automationexercise.com](https://automationexercise.com), cada una con 3
ejercicios elegidos de su enunciado, validaciones automáticas y evidencias de ejecución.

| Práctica | Herramienta | Ejercicios elegidos | Resultado | Informe |
|---|---|---|---|---|
| [1](practica-1-selenium-ide/) | Selenium IDE (`.side`) | 3 · Login incorrecto, 4 · Búsqueda, 6 · Suscripción | 3/3 aprobados | [PDF](informes/practica-1-selenium-ide.pdf) |
| [2](practica-2-selenium-webdriver/) | Selenium WebDriver + Python + pytest | 2 · Login correcto, 4 · Búsqueda, 5 · Contact Us con archivo | 3/3 aprobados | [PDF](informes/practica-2-selenium-webdriver.pdf) |
| [3](practica-3-robot-framework/robot_project/) | Robot Framework + SeleniumLibrary | 1 · Login correcto, 2 · Login incorrecto, 3 · Búsqueda | 3/3 aprobados | [PDF](informes/practica-3-robot-framework.pdf) |

Cada informe tiene la carátula de la universidad, está en formato APA 7 y contiene la explicación de los escenarios,
el código relevante, las validaciones, las capturas y los resultados.

## Estructura

```
practicas-automatizacion/
├── README.md
├── CHANGELOG.md                        cambios de cada versión
├── requirements.txt                    dependencias de Python con versión fija
├── informes/                           informe PDF de las prácticas 1, 2 y 3
├── practica-1-selenium-ide/
│   ├── Practica1_SeleniumIDE.side      proyecto de Selenium IDE (se abre en la extensión)
│   ├── generar_side.py                 genera el .side
│   ├── ejecutar_con_evidencias.py      lo reproduce con selenium-side-runner y guarda capturas
│   └── evidencias/                     pantalla final y consola de cada ejercicio
├── practica-2-selenium-webdriver/
│   ├── conftest.py                     navegador, cuenta de prueba por API y capturas
│   ├── pytest.ini                      configuración y reportes
│   ├── pages/paginas.py                Page Object Model (localizadores ID, Name, XPath y CSS)
│   ├── tests/test_ejercicios.py        los 3 ejercicios
│   ├── data/archivo_adjunto.txt        archivo que se adjunta en Contact Us
│   ├── evidencias/                     capturas PNG
│   └── reports/                        reporte HTML y JUnit
└── practica-3-robot-framework/robot_project/
    ├── tests/                          login.robot y busqueda.robot
    ├── keywords/                       comunes.resource y CuentaPrueba.py
    ├── variables/                      variables.resource
    ├── screenshots/                    capturas generadas
    └── reports/                        report.html, log.html y output.xml
```

## Instalación (Windows)

```bat
git clone https://github.com/Mirkof69/practicas-automatizacion.git
cd practicas-automatizacion
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

Chrome debe estar instalado; Selenium Manager descarga el driver solo. Para la Práctica 1 hace falta Node.js y
`npm install selenium-side-runner@4.0.13` en una carpeta **sin espacios** (o abrir el `.side` en la extensión
Selenium IDE y pulsar *Run all tests*).

## Ejecución

```bat
:: Práctica 1 · Selenium IDE (con capturas)
cd practica-1-selenium-ide && ..\.venv\Scripts\python ejecutar_con_evidencias.py

:: Práctica 2 · Selenium WebDriver (reporte en reports\reporte.html; VISIBLE=1 para ver el navegador)
cd practica-2-selenium-webdriver && ..\.venv\Scripts\python -m pytest

:: Práctica 3 · Robot Framework (reporte en reports\report.html)
cd practica-3-robot-framework\robot_project && ..\..\.venv\Scripts\python -m robot --outputdir reports tests
```

## Flujo de trabajo con Git (GitFlow)

El repositorio sigue GitFlow:

| Rama | Para qué sirve |
|---|---|
| `main` | Versiones entregadas. Cada una lleva su etiqueta (`v1.0.0`). |
| `develop` | Integración: recibe cada práctica terminada. |
| `feature/practica-1-selenium-ide` | Desarrollo de la Práctica 1. |
| `feature/practica-2-selenium-webdriver` | Desarrollo de la Práctica 2. |
| `feature/practica-3-robot-framework` | Desarrollo de la Práctica 3. |
| `feature/documentacion` | README con la instalación, la ejecución y este flujo. |
| `release/1.0.0` | Preparación de la entrega: informes en PDF y CHANGELOG. |

Cada `feature/*` nace de `develop` y vuelve a `develop` con un merge `--no-ff`, para que el historial muestre qué
commits forman cada práctica. La entrega sale de `release/1.0.0`, que se une a `main` (con la etiqueta `v1.0.0`) y
de vuelta a `develop`. Los mensajes de commit siguen el formato `tipo(ámbito): descripción`, con los tipos `feat`
(funcionalidad o prueba nueva), `test` (evidencias y reportes), `docs` (documentación) y `chore` (configuración).

```bash
git log --graph --oneline --all    # ver las ramas y los merges
```

## Decisiones

- **Cuenta de prueba por API.** El login correcto crea una cuenta nueva con la API pública del sitio
  (`POST /api/createAccount`) y la borra al terminar (`DELETE /api/deleteAccount`): no depende de datos a mano.
- **Anuncios bloqueados.** El sitio muestra anuncios de Google que tapan la página; el navegador de prueba los
  bloquea con `--host-resolver-rules`. No cambia el comportamiento del sitio.
- **Esperas explícitas**, nunca pausas fijas para esperar resultados.
