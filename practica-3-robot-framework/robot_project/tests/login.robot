*** Settings ***
Documentation     Ejercicio 1 (login correcto) y Ejercicio 2 (login incorrecto) de la Práctica 3.
...               La cuenta válida se crea por la API antes de la suite y se elimina al final.
Resource          ../keywords/comunes.resource
Suite Setup       Preparar Suite De Login
Suite Teardown    Limpiar Suite De Login
Test Teardown     Run Keyword If Test Failed    Tomar Evidencia    fallo


*** Variables ***
${CORREO_VALIDO}    ${EMPTY}


*** Test Cases ***
Ejercicio 1 - Login Correcto
    [Documentation]    Login con credenciales válidas: el usuario accede al sistema.
    [Tags]    ejercicio1    login    smoke
    Iniciar Sesion Con    ${CORREO_VALIDO}    ${CLAVE_VALIDA}
    El Usuario Deberia Estar Conectado    ${NOMBRE_USUARIO}
    Title Should Be    ${TITULO_INICIO}
    Tomar Evidencia    sesion_iniciada
    Click Link    ${ENLACE_SALIR}
    Page Should Contain Element    ${BOTON_INGRESAR}

Ejercicio 2 - Login Incorrecto
    [Documentation]    Login con credenciales inválidas: se muestra el mensaje de error del sistema.
    [Tags]    ejercicio2    login    negativo
    Iniciar Sesion Con    ${CORREO_INVALIDO}    ${CLAVE_INVALIDA}
    Deberia Mostrarse El Error De Login
    Location Should Be    ${URL_LOGIN}
    Tomar Evidencia    mensaje_error


*** Keywords ***
Preparar Suite De Login
    ${correo}=    Crear Cuenta De Prueba    ${NOMBRE_USUARIO}    ${CLAVE_VALIDA}
    Set Suite Variable    ${CORREO_VALIDO}    ${correo}
    Abrir Sitio En    ${URL_BASE}

Limpiar Suite De Login
    Cerrar Sitio
    Eliminar Cuenta De Prueba    ${CORREO_VALIDO}    ${CLAVE_VALIDA}
