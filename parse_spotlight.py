import os
import json
import urllib.request

# Crear carpeta temporal si no existe
temp_folder = "temp"
os.makedirs(temp_folder, exist_ok=True)


url = os.environ.get("EVENTS_URL")
if not url:
    raise ValueError("No se ha definido la variable de entorno EVENTS_URL")

# Descargar y parsear
response = urllib.request.urlopen(url)
events = json.loads(response.read().decode())

# Filtrar solo spotlight-hour
spotlight_events = []

for event in events:
    if event.get("eventType") == "pokemon-spotlight-hour":
        spotlight = event.get("extraData", {}).get("spotlight", {})
        simplified_list = [
            {
                "name": p["name"],
                "canBeShiny": p["canBeShiny"],
                "image": p["image"].split("/")[-1]
            }
            for p in spotlight.get("list", [])
        ]

        spotlight_events.append({
            "eventID": event.get("eventID"),
            "name": event.get("name"),
            "start": event.get("start"),
            "end": event.get("end"),
            "bonus": spotlight.get("bonus"),
            "list": simplified_list
        })

# Guardar resultado
output_path = os.path.join(temp_folder, "spotlighthour.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(spotlight_events, f, ensure_ascii=False, indent=2)

print(f"✅ Archivo generado: {output_path}")
