import os
import json
import urllib.request

# Crear carpeta temporal si no existe
temp_folder = "temp"
os.makedirs(temp_folder, exist_ok=True)

# Descargar el JSON original
url = os.environ.get("RAIDS_URL")
if not url:
    raise ValueError("No se ha definido la variable de entorno RAIDS_URL")

response = urllib.request.urlopen(url)
data = json.loads(response.read().decode())

# Mapeo personalizado
tier_map = {
    "Tier 1": "Incursiones 1",
    "Tier 2": "Incursiones 2",
    "Tier 3": "Incursiones 3",
    "Tier 5": "Incursiones 5",
    "Mega": "Mega Incursiones",
    "Shadow Tier 1": "Incursiones Oscuras Nivel 1",
    "Shadow Tier 2": "Incursiones Oscuras Nivel 2",
    "Shadow Tier 3": "Incursiones Oscuras Nivel 3",
    "Shadow Tier 5": "Incursiones Oscuras Nivel 5"
}

# Agrupar y limpiar
grouped = {}
for pkm in data:
    raw_tier = pkm.get("tier", "Unknown")
    tier = tier_map.get(raw_tier, raw_tier)
    if tier not in grouped:
        grouped[tier] = []

    grouped[tier].append({
        "name": pkm["name"],
        "canBeShiny": pkm["canBeShiny"],
        "image": pkm["image"].split("/")[-1],
        "types": [t["image"].split("/")[-1] for t in pkm["types"]],
        "boostedWeather": [w["image"].split("/")[-1] for w in pkm["boostedWeather"]],
        "combatPower": pkm["combatPower"]
    })

# Guardar el archivo
json_file_path = os.path.join(temp_folder, "bossraid.json")
with open(json_file_path, "w", encoding="utf-8") as f:
    json.dump(grouped, f, ensure_ascii=False, indent=2)
print("✅ Archivo bossraid.json generado en temp/")
