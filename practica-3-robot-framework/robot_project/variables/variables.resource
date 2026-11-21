*** Settings ***
Documentation     Variables reutilizables de la Práctica 3: sitio, navegador, datos de prueba y localizadores.


*** Variables ***
# --- sitio y navegador
${URL_BASE}                 https://automationexercise.com
${URL_LOGIN}                ${URL_BASE}/login
${URL_PRODUCTOS}            ${URL_BASE}/products
${API}                      ${URL_BASE}/api
${NAVEGADOR}                chrome
${ESPERA}                   15s
# Los anuncios de Google del sitio abren ventanas que tapan la página: se bloquean en el navegador de prueba
${SIN_ANUNCIOS}             MAP googleads.g.doubleclick.net 127.0.0.1, MAP *.doubleclick.net 127.0.0.1, MAP *.googlesyndication.com 127.0.0.1, MAP adservice.google.com 127.0.0.1, MAP *.adtrafficquality.google 127.0.0.1, MAP fundingchoicesmessages.google.com 127.0.0.1
${OPCIONES_CHROME}          add_argument("--headless=new");add_argument("--window-size=1366,900");add_argument("--host-resolver-rules=${SIN_ANUNCIOS}")

# --- datos de prueba
${NOMBRE_USUARIO}           QA Robot
${CLAVE_VALIDA}             Clave.Robot.2026
${CORREO_INVALIDO}          no.existe.robot@example.com
${CLAVE_INVALIDA}           ClaveIncorrecta.123
${MENSAJE_ERROR_LOGIN}      Your email or password is incorrect!
${TERMINO_BUSQUEDA}         saree
${TITULO_LOGIN}             Automation Exercise - Signup / Login
${TITULO_INICIO}            Automation Exercise

# --- localizadores (id, name, css y xpath)
${CAMPO_CORREO}             css:input[data-qa='login-email']
${CAMPO_CLAVE}              name:password
${BOTON_INGRESAR}           xpath://button[@data-qa='login-button']
${USUARIO_CONECTADO}        xpath://a[contains(., 'Logged in as')]
${ENLACE_SALIR}             css:a[href='/logout']
${ERROR_LOGIN}              xpath://form[@action='/login']/p
${BUSCADOR}                 id:search_product
${BOTON_BUSCAR}             id:submit_search
${TITULO_SECCION}           xpath://h2[@class='title text-center']
${NOMBRES_PRODUCTOS}        css:.features_items .productinfo p
