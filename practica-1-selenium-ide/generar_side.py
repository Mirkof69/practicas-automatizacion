"""Genera Practica1_SeleniumIDE.side (formato 2.0 de Selenium IDE) con los 3 ejercicios elegidos de la Práctica 1:

  Ejercicio 3 · Inicio de sesión incorrecto   → valida el mensaje de error
  Ejercicio 4 · Búsqueda de productos         → valida que existan resultados relacionados
  Ejercicio 6 · Suscripción por correo        → valida el mensaje de éxito

El archivo se abre tal cual en la extensión Selenium IDE (Chrome o Firefox): Open project → Practica1_SeleniumIDE.side.

    python generar_side.py
"""
import json
import uuid
from pathlib import Path

URL = "https://automationexercise.com"
SALIDA = Path(__file__).resolve().parent / "Practica1_SeleniumIDE.side"


def _id(*partes: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "practica1-ide/" + "/".join(partes)))


def c(comando: str, objetivo: str = "", valor: str = "", comentario: str = "") -> dict:
    return {"command": comando, "target": objetivo, "value": valor, "comment": comentario}


EJERCICIOS = [
    ("Ejercicio 3 - Inicio de sesion incorrecto", [
        c("open", "/login", comentario="Página de login"),
        c("setWindowSize", "1366x900"),
        c("verifyTitle", "Automation Exercise - Signup / Login", comentario="VALIDACIÓN: estamos en el login"),
        c("assertElementPresent", "css=input[data-qa='login-email']", comentario="VALIDACIÓN: existe el campo correo"),
        c("type", "css=input[data-qa='login-email']", "qa.ide.no.existe@example.com", "Correo que no está registrado"),
        c("type", "name=password", "ClaveIncorrecta.123", "Contraseña incorrecta"),
        c("click", "css=button[data-qa='login-button']", comentario="Pulsar Login"),
        c("waitForElementVisible", "xpath=//form[@action='/login']/p", "15000", "Espera el mensaje de error"),
        c("assertText", "xpath=//form[@action='/login']/p", "Your email or password is incorrect!",
          "VALIDACIÓN: mensaje de error exacto"),
        c("assertElementNotPresent", "css=a[href='/logout']", comentario="VALIDACIÓN: no inició sesión (no hay Logout)"),
    ]),
    ("Ejercicio 4 - Busqueda de productos", [
        c("open", "/products", comentario="Página de productos"),
        c("setWindowSize", "1366x900"),
        c("assertText", "xpath=//h2[@class='title text-center']", "ALL PRODUCTS", "VALIDACIÓN: listado completo"),
        c("type", "id=search_product", "dress", "Término de búsqueda"),
        c("click", "id=submit_search", comentario="Pulsar buscar"),
        c("waitForText", "xpath=//h2[@class='title text-center']", "SEARCHED PRODUCTS", "Espera los resultados"),
        c("assertText", "xpath=//h2[@class='title text-center']", "SEARCHED PRODUCTS", "VALIDACIÓN: título de resultados"),
        c("assertElementPresent", "xpath=//div[@class='productinfo text-center']/p[contains(., 'Dress')]",
          comentario="VALIDACIÓN: hay al menos un producto relacionado con «dress»"),
        c("executeScript", "return document.querySelectorAll('.features_items .productinfo').length > 0",
          "hayResultados", "Cuenta los productos mostrados"),
        c("assert", "hayResultados", "true", "VALIDACIÓN: la búsqueda devolvió resultados"),
    ]),
    ("Ejercicio 6 - Suscripcion por correo", [
        c("open", "/", comentario="Página de inicio"),
        c("setWindowSize", "1366x900"),
        c("assertElementPresent", "id=susbscribe_email", comentario="VALIDACIÓN: existe el campo de suscripción"),
        c("type", "id=susbscribe_email", "qa.ide.suscripcion@example.com", "Correo para suscribirse"),
        c("click", "id=subscribe", comentario="Pulsar la flecha de suscripción"),
        c("waitForElementVisible", "id=success-subscribe", "15000", "Espera el mensaje de éxito"),
        c("assertText", "css=#success-subscribe .alert-success", "You have been successfully subscribed!",
          "VALIDACIÓN: mensaje de éxito exacto"),
        c("executeScript", "document.getElementById('success-subscribe').scrollIntoView({block: 'center'})",
          comentario="Lleva el mensaje a la vista para la evidencia"),
        c("pause", "800", comentario="Deja ver el mensaje antes de terminar"),
    ]),
]


def construir() -> dict:
    pruebas = [{"id": _id(nombre), "name": nombre,
                "commands": [{"id": _id(nombre, str(i)), "comment": x["comment"], "command": x["command"],
                              "target": x["target"], "targets": [], "value": x["value"]} for i, x in enumerate(cmds)]}
               for nombre, cmds in EJERCICIOS]
    suite = {"id": _id("suite"), "name": "Practica 1 - Selenium IDE", "persistSession": False, "parallel": False,
             "timeout": 300, "tests": [p["id"] for p in pruebas]}
    return {"id": _id("proyecto"), "version": "2.0", "name": "Practica 1 - Selenium IDE", "url": URL,
            "tests": pruebas, "suites": [suite], "urls": [URL + "/"], "plugins": []}


if __name__ == "__main__":
    SALIDA.write_text(json.dumps(construir(), ensure_ascii=False, indent=2), encoding="utf-8")
    print(SALIDA)
