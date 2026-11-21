"""Librería de keywords en Python: crea y borra una cuenta de prueba con la API pública del sitio.

Así el login correcto no depende de una cuenta creada a mano: cada ejecución usa una cuenta nueva y la elimina.
"""
from datetime import datetime

import requests
from robot.api.deco import keyword, library


@library(scope="SUITE")
class CuentaPrueba:
    def __init__(self, api: str = "https://automationexercise.com/api"):
        self.api = api

    @keyword("Crear Cuenta De Prueba")
    def crear(self, nombre: str, clave: str) -> str:
        """Crea la cuenta y devuelve su correo (único por ejecución)."""
        correo = f"qa.robot.{datetime.now():%Y%m%d%H%M%S}@example.com"
        datos = {"name": nombre, "email": correo, "password": clave, "title": "Mr", "birth_date": "10",
                 "birth_month": "5", "birth_year": "1999", "firstname": "QA", "lastname": "Robot",
                 "company": "UNIFRANZ", "address1": "Av. Prueba 123", "address2": "", "country": "United States",
                 "zipcode": "10001", "state": "New York", "city": "New York", "mobile_number": "70000000"}
        r = requests.post(f"{self.api}/createAccount", data=datos, timeout=30).json()
        if r.get("responseCode") != 201:
            raise AssertionError(f"No se pudo crear la cuenta de prueba: {r}")
        return correo

    @keyword("Eliminar Cuenta De Prueba")
    def eliminar(self, correo: str, clave: str) -> None:
        requests.delete(f"{self.api}/deleteAccount", data={"email": correo, "password": clave}, timeout=30)
