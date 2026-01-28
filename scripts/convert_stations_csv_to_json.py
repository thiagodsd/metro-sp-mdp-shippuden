import pandas as pd
import json

csv_path = '/home/dusoudeth/Documentos/github/metro-sp-mdp/data/03_primary/metrosp_stations.csv'
json_path = '/home/dusoudeth/Documentos/github/metro-sp-mdp-shippuden/frontend/public/data/stations.json'

df = pd.read_csv(csv_path)
df_clean = df[['name', 'lat', 'lon', 'cor']].copy()
df_clean.columns = ['name', 'lat', 'lon', 'color']

stations = df_clean.to_dict('records')

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(stations, f, ensure_ascii=False, indent=2)

print(f"Convertido {len(stations)} estações para JSON")
print(f"Arquivo salvo em: {json_path}")
