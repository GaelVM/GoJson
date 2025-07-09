import os
import json
import urllib.request

# Crear carpeta temporal si no existe
temp_folder = "temp"
os.makedirs(temp_folder, exist_ok=True)

# Leer la URL desde variable de entorno
url = os.environ.get("EVENTS_URL")
if not url:
    raise ValueError("No se ha definido la variable de entorno EVENTS_URL")

# Descargar y parsear
response = urllib.request.urlopen(url)
events = json.loads(response.read().decode())

# Filtrar tipo raid-hour
raid_hour_events = []

for event in events:
    if event.get("eventType") == "raid-hour":
        full_name = event.get("name", "")
        pokemon_name = full_name.replace(" Raid Hour", "").strip()

        raid_hour_events.append({
            "eventID": event.get("eventID"),
            "name": pokemon_name,
            "start": event.get("start"),
            "end": event.get("end")
        })

# Guardar archivo en temp/
output_path = os.path.join(temp_folder, "raidhour.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(raid_hour_events, f, ensure_ascii=False, indent=2)

print(f"✅ Archivo generado: {output_path}")
