
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from html import unescape
from zoneinfo import ZoneInfo

URL = "https://www.sunat.gob.pe/mensajes/mensajes-SUNAT.html"

req = Request(URL, headers={
    "User-Agent": "Mozilla/5.0 (compatible; ESIntegralRadar/1.0)"
})

with urlopen(req, timeout=30) as respuesta:
    html = respuesta.read().decode("utf-8", errors="replace")

# Extraer texto visible y buscar comunicados con fecha
html = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", html,
              flags=re.I | re.S)
html = re.sub(r"<[^>]+>", " ", html)
texto = unescape(re.sub(r"\s+", " ", html))

patron = r"(\d{2}/\d{2}/2026)\s+(.{20,350}?)(?=\d{2}/\d{2}/2026|$)"
coincidencias = re.findall(patron, texto)

novedades = []
for fecha, titulo in coincidencias[:20]:
    novedades.append({
        "fecha": fecha,
        "titulo": titulo.strip(),
        "fuente": "SUNAT",
        "categoria": "Tributario",
        "tipo": "Comunicado",
        "url": URL,
        "estado_verificacion": "Pendiente de revisión"
    })

resultado = {
    "ultima_actualizacion": datetime.now(
        ZoneInfo("America/Lima")
    ).isoformat(),
    "fuente": URL,
    "novedades": novedades
}

destino = Path(__file__).parent / "novedades.json"
destino.write_text(
    json.dumps(resultado, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Comunicados detectados: {len(novedades)}")
print(f"Archivo generado: {destino}")
