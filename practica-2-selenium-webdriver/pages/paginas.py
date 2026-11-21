"""Page Object Model: cada página del sitio con sus localizadores y acciones.

Se usan los cuatro tipos de localizador pedidos: ID, NAME, XPATH y CSS_SELECTOR (anotado en cada uno).
"""
from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://automationexercise.com"


class Pagina:
    def __init__(self, driver, espera: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, espera)

    def visible(self, loc):
        return self.wait.until(EC.visibility_of_element_located(loc))

    def clic(self, loc):
        self.wait.until(EC.element_to_be_clickable(loc)).click()

    def escribir(self, loc, texto: str):
        campo = self.visible(loc)
        campo.clear()
        campo.send_keys(texto)


class LoginPage(Pagina):
    CORREO = (By.CSS_SELECTOR, "input[data-qa='login-email']")          # CSS Selector (hay dos name="email")
    CLAVE = (By.NAME, "password")                                       # Name
    INGRESAR = (By.XPATH, "//button[@data-qa='login-button']")          # XPath
    ERROR = (By.XPATH, "//form[@action='/login']/p")                    # XPath

    def abrir(self):
        self.driver.get(f"{BASE_URL}/login")
        return self

    def ingresar(self, correo: str, clave: str):
        self.escribir(self.CORREO, correo)
        self.escribir(self.CLAVE, clave)
        self.clic(self.INGRESAR)


class MenuSuperior(Pagina):
    USUARIO = (By.XPATH, "//a[contains(., 'Logged in as')]")            # XPath
    SALIR = (By.CSS_SELECTOR, "a[href='/logout']")                      # CSS Selector

    def usuario(self) -> str:
        return self.visible(self.USUARIO).text
