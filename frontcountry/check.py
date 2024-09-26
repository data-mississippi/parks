import requests
import json


available = []
front_country_sites = [
    {'Two Medicine Campground': '258799'},
    {'ST. MARY CAMPGROUND': '232492'},
    {'APGAR GROUP SITES': '234669'},
    {'MANY GLACIER CAMPGROUND': '251869'},
    {'Sprague Creek Campground': '258795'},
    {'Apgar Campground': '10171274'},
    {'Avalanche Campground': '258796'},
    {'FISH CREEK CAMPGROUND': '232493'},
]
trips = [{'start_date': '', 'end_date': '', 'sites': [front_country_sites]}]

# start_date=2023-07-21T00%3A00%3A00Z&end_date=2023-07-25T00%3A00%3A00Z
# fq=campsite_type_of_use%3ADay&fq=entity_type%3Acampground&fq=parent_asset_id%3A2725

# params =
# q=Glacier%20National%20Park
# entity_id=2725

# glacier_front_country = {
#     'parent_asset_id': 2725,
#     # 'campsite_type_of_use': 'Day',
#     # 'entity_type': 'campground',
#     # 'campsite_type_of_use': 'Overnight',
#     # '-entity_type': 'A(tour OR timedentry_tour)',
#     'size': 300,
#     'entity_type': 'recarea',
#     'entity_id': 4675321030,
#     'q': 'Glacier National Park',
# }
# 4675321
for trip in trips:

    url = 'https://www.recreation.gov/api/search/geo?q=Glacier%20National%20Park&entity_id=2725&entity_type=recarea&size=300&fq=-entity_type%3A(tour%20OR%20timedentry_tour)&fq=campsite_type_of_use%3AOvernight&fq=campsite_type_of_use%3Ana&fq=entity_type%3Acampground&fq=campsite_type_of_use%3ADay&fq=entity_type%3Acampground&fq=parent_asset_id%3A2725&start_date=2023-07-21T00%3A00%3A00Z&end_date=2023-07-25T00%3A00%3A00Z'
    response = requests.get(
        url,
        headers={
            'Referer': 'https://www.recreation.gov/camping/gateways/2725',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/111.0',
        },
    )

    for campsite in response.json()['results']:
        name = campsite['name']
        if (
            campsite['availability'] != 'unavailable'
        ):  # dunno what available looks like bc none are, prob "available" but not gonna chance it
            available.append(
                {
                    name: {
                        'status': campsite['availability'],
                        'url': f'https://www.recreation.gov/camping/campgrounds/{campsite["entity_id"]}',
                    }
                }
            )

    if available:
        raise Exception(
            f'These campsites are available: {json.dumps(available)}'
        )  # this will crash the action and i'll get an email
