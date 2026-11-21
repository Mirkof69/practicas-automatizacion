r"""Reproduce cada ejercicio del .side con selenium-side-runner (el ejecutor oficial de Selenium IDE) y guarda:

  evidencias/<ejercicio>.png        pantalla del navegador al terminar el ejercicio (después de sus validaciones)
  evidencias/<ejercicio>_consola.png  salida del ejecutor con el resultado (passed / failed)
  evidencias/resultados.json        estado, duración y salida de cada ejercicio

Las imágenes se toman por el protocolo DevTools de Chrome (puerto de depuración) mientras corre la prueba.

    ..\.venv\Scripts\python ejecutar_con_evidencias.py
Requiere selenium-side-runner 4.0.13 (npm) en una carpeta SIN espacios; por defecto
%LOCALAPPDATA%\fetal-medical\side_runner (variable SIDE_RUNNER para otra ruta).
"""
from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import threading
import time
import urllib.request
from pathlib import Path

import websocket
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
SIDE = AQUI / "Practica1_SeleniumIDE.side"
EVIDENCIAS = AQUI / "evidencias"
RUNNER = Path(os.environ.get("SIDE_RUNNER", Path(os.environ["LOCALAPPDATA"]) / "fetal-medical" / "side_runner"
                             / "node_modules" / ".bin" / "selenium-side-runner.cmd"))
PUERTO = 9341
SIN_ANUNCIOS = ("MAP googleads.g.doubleclick.net 127.0.0.1;MAP *.doubleclick.net 127.0.0.1;"
                "MAP *.googlesyndication.com 127.0.0.1;MAP adservice.google.com 127.0.0.1")


class Capturador(threading.Thread):
    """Toma la pantalla de la pestaña activa cada 0,4 s y conserva la última imagen."""

    def __init__(self):
        super().__init__(daemon=True)
        self.ultima: bytes | None = None
        self.alto = threading.Event()

    def run(self):
        ws, n = None, 0
        while not self.alto.is_set():
            try:
                if ws is None:
                    with urllib.request.urlopen(f"http://127.0.0.1:{PUERTO}/json", timeout=1) as r:
                        paginas = [t for t in json.load(r) if t.get("type") == "page"]
                    if paginas:
                        ws = websocket.create_connection(paginas[0]["webSocketDebuggerUrl"].replace("localhost", "127.0.0.1"),
                                                         timeout=2, suppress_origin=True)
                if ws is not None:
                    n += 1
                    ws.send(json.dumps({"id": n, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
                    while True:
                        m = json.loads(ws.recv())
                        if m.get("id") == n:
                            break
                    if "result" in m:
                        self.ultima = base64.b64decode(m["result"]["data"])
            except Exception:   # el navegador arranca o se cierra: se reintenta
                ws = None
            self.alto.wait(0.4)


def consola_a_imagen(texto: str, destino: Path, titulo: str):
    fuente = ImageFont.truetype("consola.ttf", 15) if Path(r"C:\Windows\Fonts\consola.ttf").exists() else ImageFont.load_default()
    texto = re.sub(r"\x1b\[[0-9;]*m|\[[0-9;]*m", "", texto)   # códigos de color de la consola
    ruido = ("DeprecationWarning", "--trace-deprecation", "Jest did not exit", "asynchronous operations",
             "Ran all test suites", "doesn't have any suites matching", "attempting to iterate", "at src/main",
             "at Array.forEach", "console.info")
    lineas = [titulo, ""] + [x for x in texto.splitlines() if x.strip() and not any(r in x for r in ruido)][-24:]
    img = Image.new("RGB", (1100, 30 + 22 * len(lineas)), "#0f1a1c")
    d = ImageDraw.Draw(img)
    for i, linea in enumerate(lineas):
        color = "#5fd39a" if re.search(r"pass|✓", linea, re.I) else "#ff8a7e" if re.search(r"fail|✕", linea, re.I) else "#cfe0dd"
        d.text((16, 14 + 22 * i), linea[:120], font=fuente, fill="#8fd3ff" if i == 0 else color)
    img.save(destino)


def ejecutar(nombre: str) -> dict:
    capacidades = (f"browserName=chrome goog:chromeOptions.args=[--headless=new,--window-size=1366,900,"
                   f"--remote-debugging-port={PUERTO},--host-resolver-rules={SIN_ANUNCIOS}]")
    cap = Capturador()
    cap.start()
    t0 = time.perf_counter()
    p = subprocess.run([str(RUNNER), "-c", capacidades, "--filter", f"^{re.escape(nombre)}$", "--timeout", "30000",
                        str(SIDE)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
    cap.alto.set()
    salida = (p.stdout + p.stderr).strip()
    estado = "PASS" if re.search(r"Tests:\s+1 passed", salida) else "FAIL"
    base = re.sub(r"[^A-Za-z0-9]+", "_", nombre).strip("_")
    if cap.ultima:
        (EVIDENCIAS / f"{base}.png").write_bytes(cap.ultima)
    consola_a_imagen(salida, EVIDENCIAS / f"{base}_consola.png", f"selenium-side-runner · {nombre} · {estado}")
    return {"ejercicio": nombre, "estado": estado, "duracion_s": round(time.perf_counter() - t0, 1), "salida": salida[-3000:]}


if __name__ == "__main__":
    EVIDENCIAS.mkdir(exist_ok=True)
    proyecto = json.loads(SIDE.read_text(encoding="utf-8"))
    resultados = [ejecutar(t["name"]) for t in proyecto["tests"]]
    (EVIDENCIAS / "resultados.json").write_text(json.dumps(resultados, ensure_ascii=False, indent=1), encoding="utf-8")
    for r in resultados:
        print(f"{r['estado']:5} {r['duracion_s']:6} s  {r['ejercicio']}")
