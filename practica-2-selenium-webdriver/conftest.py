"""Configuración común de la Práctica 2 (Selenium WebDriver + Python + pytest).

- navegador: Chrome con Selenium Manager (descarga el driver solo); anuncios bloqueados para que no tapen la página.
- cuenta_prueba: crea una cuenta nueva por la API pública del sitio antes del ejercicio y la borra al terminar,
  así el login correcto no depende de una cuenta creada a mano.
- captura: guarda una captura PNG con nombre ordenado en evidencias/.
"""
from __future__ import annotations

import os
import time
from datetime import datetime
from pathlib import Path

import pytest
import requests
from selenium import webdriver

BASE_URL = "https://automationexercise.com"
API = f"{BASE_URL}/api"
RAIZ = Path(__file__).resolve().parent
EVIDENCIAS = RAIZ / "evidencias"

# Los anuncios de Google del sitio abren ventanas que tapan la página y vuelven inestable la prueba.
DOMINIOS_ANUNCIOS = ["googleads.g.doubleclick.net", "*.doubleclick.net", "pagead2.googlesyndication.com",
                     "*.googlesyndication.com", "adservice.google.com", "*.adtrafficquality.google",
                     "fundingchoicesmessages.google.com"]


@pytest.fixture
def navegador():
    opciones = webdriver.ChromeOptions()
    if os.environ.get("VISIBLE") != "1":
        opciones.add_argument("--headless=new")
    opciones.add_argument("--window-size=1366,900")
    opciones.add_argument("--host-resolver-rules=" + ", ".join(f"MAP {d} 127.0.0.1" for d in DOMINIOS_ANUNCIOS))
    driver = webdriver.Chrome(options=opciones)
    driver.implicitly_wait(0)
    yield driver
    driver.quit()


@pytest.fixture
def cuenta_prueba():
    """Cuenta nueva creada por la API (POST /api/createAccount) y borrada al final (DELETE /api/deleteAccount)."""
    marca = datetime.now().strftime("%Y%m%d%H%M%S")
    datos = {"name": "QA Practica", "email": f"qa.practica.{marca}@example.com", "password": "Clave.Prueba.2026",
             "title": "Mr", "birth_date": "10", "birth_month": "5", "birth_year": "1999", "firstname": "QA",
             "lastname": "Practica", "company": "UNIFRANZ", "address1": "Av. Prueba 123", "address2": "",
             "country": "United States", "zipcode": "10001", "state": "New York", "city": "New York",
             "mobile_number": "70000000"}
    r = requests.post(f"{API}/createAccount", data=datos, timeout=30).json()
    assert r.get("responseCode") == 201, f"No se pudo crear la cuenta de prueba: {r}"
    yield datos
    requests.delete(f"{API}/deleteAccount", data={"email": datos["email"], "password": datos["password"]},
                    timeout=30)


@pytest.fixture
def captura(navegador, request):
    """captura("nombre") guarda evidencias/<ejercicio>_<n>_<nombre>.png y devuelve la ruta."""
    EVIDENCIAS.mkdir(exist_ok=True)
    contador = {"n": 0}
    ejercicio = request.node.name.removeprefix("test_")

    def tomar(nombre: str) -> Path:
        contador["n"] += 1
        time.sleep(0.3)   # deja terminar la animación del mensaje antes de la foto (no es una espera de la prueba)
        ruta = EVIDENCIAS / f"{ejercicio}_{contador['n']}_{nombre}.png"
        navegador.save_screenshot(str(ruta))
        return ruta
    return tomar
