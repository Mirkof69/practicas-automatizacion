*** Settings ***
Documentation     Ejercicio 3 de la Práctica 3: búsqueda de productos.
Resource          ../keywords/comunes.resource
Suite Setup       Abrir Sitio En    ${URL_BASE}
Suite Teardown    Cerrar Sitio
Test Teardown     Run Keyword If Test Failed    Tomar Evidencia    fallo


*** Test Cases ***
Ejercicio 3 - Busqueda De Productos
    [Documentation]    Buscar en Productos y validar que cada resultado corresponda al término buscado.
    [Tags]    ejercicio3    productos    smoke
    Buscar Producto    ${TERMINO_BUSQUEDA}
    Element Should Be Visible    ${NOMBRES_PRODUCTOS}
    Los Resultados Deberian Corresponder A    ${TERMINO_BUSQUEDA}
    Tomar Evidencia    resultados
