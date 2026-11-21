*** Settings ***
Documentation     Keywords personalizadas reutilizables: navegador, login, búsqueda y evidencias.
Library           SeleniumLibrary    timeout=15s
Library           String
Library           ${CURDIR}/CuentaPrueba.py
Resource          ../variables/variables.resource


*** Keywords ***
# --- navegador y evidencias
Abrir Sitio En
    [Documentation]    Abre Chrome sin anuncios en la URL indicada y fija la carpeta de capturas.
    [Arguments]    ${url}
    Set Screenshot Directory    ${CURDIR}/../screenshots
    Open Browser    ${url}    ${NAVEGADOR}    options=${OPCIONES_CHROME}
    Set Selenium Timeout    ${ESPERA}

Cerrar Sitio
    Close All Browsers

Tomar Evidencia
    [Documentation]    Captura con nombre ordenado: <prueba>_<paso>.png en screenshots/.
    [Arguments]    ${paso}
    ${nombre}=    Replace String Using Regexp    ${TEST NAME}    [^A-Za-z0-9]+    _
    Capture Page Screenshot    ${nombre}_${paso}.png

# --- login
Iniciar Sesion Con
    [Documentation]    Completa el formulario de login y envía.
    [Arguments]    ${correo}    ${clave}
    Go To    ${URL_LOGIN}
    Title Should Be    ${TITULO_LOGIN}
    Input Text    ${CAMPO_CORREO}    ${correo}
    Input Password    ${CAMPO_CLAVE}    ${clave}
    Click Button    ${BOTON_INGRESAR}

El Usuario Deberia Estar Conectado
    [Arguments]    ${nombre}
    Element Should Be Visible    ${USUARIO_CONECTADO}
    Element Text Should Be    ${USUARIO_CONECTADO}    Logged in as ${nombre}
    Page Should Contain Element    ${ENLACE_SALIR}

Deberia Mostrarse El Error De Login
    Element Should Be Visible    ${ERROR_LOGIN}
    Element Text Should Be    ${ERROR_LOGIN}    ${MENSAJE_ERROR_LOGIN}
    Page Should Not Contain Element    ${ENLACE_SALIR}

# --- productos
Buscar Producto
    [Arguments]    ${termino}
    Go To    ${URL_PRODUCTOS}
    Element Text Should Be    ${TITULO_SECCION}    ALL PRODUCTS
    Input Text    ${BUSCADOR}    ${termino}
    Click Button    ${BOTON_BUSCAR}
    Wait Until Element Contains    ${TITULO_SECCION}    SEARCHED PRODUCTS

Los Resultados Deberian Corresponder A
    [Documentation]    Hay al menos un resultado y el nombre de cada producto contiene el término buscado.
    [Arguments]    ${termino}
    Page Should Contain    Searched Products
    ${productos}=    Get WebElements    ${NOMBRES_PRODUCTOS}
    ${cantidad}=    Get Length    ${productos}
    Should Be True    ${cantidad} > 0    La búsqueda de "${termino}" no devolvió productos
    FOR    ${producto}    IN    @{productos}
        ${nombre}=    Get Text    ${producto}
        ${nombre}=    Convert To Lower Case    ${nombre}
        Should Contain    ${nombre}    ${termino}    El producto "${nombre}" no corresponde a la búsqueda
    END
    Log    ${cantidad} productos encontrados para "${termino}"
