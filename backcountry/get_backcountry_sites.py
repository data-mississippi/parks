import requests
import sys
import json
import re



with open('data/finished/permit_content.json') as f:
    data = json.load(f)['payload']['divisions']

skip_sites = [
    'AEF - Elizabeth Lake Foot Administrative Site',
    'AGC - Gable Creek Administrative Site',
    'AHO - Hole in the Wall (Admin. Site)',
    'AFM - Fifty Mountain Administrative Site',
]

campsites = {}

for division_id, division in data.items():
    campsite = division['name']

    if re.match(r'[A-Z]+\s-', campsite) and campsite not in skip_sites:
        campsites.update(
            {division_id: {'district': division['district'], 'campsite': campsite}}
        )

sys.stdout.write(json.dumps(campsites))
