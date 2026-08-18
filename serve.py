# -*- coding: utf-8 -*-
r"""
serve.py — servidor local del dashboard CON proxy a Valhalla.

Sirve los archivos estáticos de `dashboard/` Y reenvía las peticiones POST a `/valhalla/*`
hacia el Valhalla local (http://localhost:8002). Así el navegador puede pedir la ISÓCRONA REAL
(por red vial) al dibujar un polígono, sin problemas de CORS (todo es mismo origen :8777).

Uso (con el Python de QGIS, o cualquier Python 3):
  & "C:\Program Files\QGIS 3.44.8\bin\python-qgis-ltr.bat" dashboard\serve.py
  # luego abrir http://localhost:8777/index.html

Si en su lugar usas `python -m http.server 8777`, el dibujo cae a la aproximación por radio
(Turf buffer): funciona, pero NO sigue la red vial. Para la isócrona real usa este serve.py
(con Valhalla arriba) o corre el script 15 sobre el GeoJSON/KML descargado.
"""
import os
import json
import http.server
import socketserver
import urllib.request
import urllib.error

PORT = 8777
VALHALLA = "http://localhost:8002"
ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def _proxy(self):
        target = VALHALLA + self.path[len("/valhalla"):]  # /valhalla/isochrone -> /isochrone
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        try:
            req = urllib.request.Request(
                target, data=body,
                headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:  # Valhalla abajo / sin datos en el punto
            msg = json.dumps({"error": str(e)}).encode("utf-8")
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)

    def do_POST(self):
        if self.path.startswith("/valhalla/"):
            self._proxy()
        else:
            self.send_response(405); self.end_headers()

    def log_message(self, fmt, *args):
        pass  # silencioso


if __name__ == "__main__":
    os.chdir(ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Dashboard + proxy Valhalla en http://localhost:%d  (Ctrl+C para salir)" % PORT)
        httpd.serve_forever()
