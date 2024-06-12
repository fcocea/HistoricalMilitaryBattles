import os
import json


def read_geojsons():
    data = []
    for file in os.listdir(os.path.join(os.path.dirname(__file__), '../gjsons')):
        if file.endswith('.geojson'):
            with open(os.path.join(os.path.dirname(__file__), '../gjsons', file), 'r') as f:
                data.append(json.load(f))
    return data


new_data = {
    "type": "FeatureCollection",
    "features": []
}

for geojson in read_geojsons():
    if 'features' in geojson:
        new_data['features'].extend(geojson['features'])
    else:
        new_data['features'].append(geojson)

with open(os.path.join(os.path.dirname(__file__), 'countries_clean.geojson'), 'r') as f:
    new_data['features'].extend(json.load(f)['features'])

with open(os.path.join(os.path.dirname(__file__), 'concat.geojson'), 'w') as f:
    json.dump(new_data, f)
