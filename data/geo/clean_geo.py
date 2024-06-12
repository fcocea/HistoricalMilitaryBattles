import json
import os


def read_geojson():
    with open(os.path.join(os.path.dirname(__file__), 'countries.geojson'), 'r') as f:
        return json.load(f)


data = read_geojson()

countries = [
    {"name": "France", "code": "FRA"},
    {"name": "Hungary", "code": "HUN"},
    {"name": "Austria", "code": "AUT"},
    {"name": "Poland", "code": "POL"},
    {"name": "Germany", "code": "DEU"},
    {"name": "Netherlands", "code": "NLD"},
    {"name": "Ireland", "code": "IRL"},
    {"name": "Russia", "code": "RUS"},
    {"name": "Egypt", "code": "EGY"},
    {"name": "Palestine", "code": "PSE"},
    {"name": "Switzerland", "code": "CHE"},
    {"name": "Portugal", "code": "PRT"},
    {"name": "Spain", "code": "ESP"},
    {"name": "Belgium", "code": "BEL"},
    {"name": "Venezuela", "code": "VEN"},
    {"name": "Peru", "code": "PER"},
    {"name": "Mexico", "code": "MEX"},
    {"name": "Sudan", "code": "SDN"},
    {"name": "Ethiopia", "code": "ETH"},
    {"name": "South Africa", "code": "ZAF"},
    {"name": "Canada", "code": "CAN"},
    {"name": "Cuba", "code": "CUB"},
    {"name": "Finland", "code": "FIN"},
    {"name": "Serbia", "code": "SRB"},
    {"name": "Turkey", "code": "TUR"},
    {"name": "Tunisia", "code": "TUN"},
    {"name": "Italy", "code": "ITA"},
    {"name": "Luxembourg", "code": "LUX"},
    {"name": "Malaysia", "code": "MYS"},
    {"name": "Japan", "code": "JPN"},
    {"name": "Jordan", "code": "JOR"},
    {"name": "Syria", "code": "SYR"},
    {"name": "Lebanon", "code": "LBN"},
    {"name": "Vietnam", "code": "VNM"}
]

new_data = {
    "type": "FeatureCollection",
    "features": []
}

found = []
for country in countries:
    for feature in data['features']:
        if feature['properties']['ISO_A3'] == country['code']:
            new_data['features'].append({
                "type": "Feature",
                "properties": {
                    "name": country['name']
                },
                "geometry": feature['geometry']

            })
            found.append(country['name'])
            break

for country in countries:
    if country['name'] not in found:
        print(f"Country not found: {country['name']}")

with open(os.path.join(os.path.dirname(__file__), 'countries_clean.geojson'), 'w') as f:
    json.dump(new_data, f)
