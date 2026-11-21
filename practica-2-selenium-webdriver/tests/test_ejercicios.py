"""Práctica 2 · Selenium WebDriver con Python. Ejercicios elegidos: 2 (login correcto), 4 (búsqueda de productos)
y 5 (Contact Us con archivo adjunto). Cada ejercicio tiene al menos 2 asserts y al menos 1 captura.
"""
from __future__ import annotations

from pathlib import Path

from pages.paginas import BASE_URL, ContactoPage, LoginPage, MenuSuperior, ProductosPage

ADJUNTO = Path(__file__).resolve().parents[1] / "data" / "archivo_adjunto.txt"


def test_ej2_login_correcto(navegador, cuenta_prueba, captura):
    """Ejercicio 2: login con credenciales válidas y validación de que el usuario ingresó al sistema."""
    login = LoginPage(navegador).abrir()
    assert "Automation Exercise - Signup / Login" == navegador.title             # assert 1: página de login
    captura("formulario_login")
    login.ingresar(cuenta_prueba["email"], cuenta_prueba["password"])

    menu = MenuSuperior(navegador)
    usuario = menu.usuario()
    captura("sesion_iniciada")
    assert usuario == f"Logged in as {cuenta_prueba['name']}"                   # assert 2: nombre del usuario
    assert menu.visible(menu.SALIR).is_displayed()                               # assert 3: aparece «Logout»
    assert navegador.current_url.rstrip("/") == BASE_URL                         # assert 4: volvió al inicio
