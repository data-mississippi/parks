import sys
import json
import requests

from util.models import Campsite

sites_file = sys.argv[1]

with open(sites_file) as f:
    sites = json.load(f)

permit_itenerary_url = 'https://www.recreation.gov/api/permititinerary/4675321/division/{division_id}/availability/month?month={month}&year={year}'
year = 2023

campsites = {}

for site_id, site in sites.items():
    campsite = Campsite(
        name=site['campsite'],
        district=site['district'],
        division_id=site_id,
    )

    for month in []:

        url = permit_itenerary_url.format(
            division_id=campsite.division_id, month=month, year=year
        )
        response = requests.get(
            url,
            headers={
                'Accept-Language': 'en-US',
                'Host': 'www.recreation.gov',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:109.0) Gecko/20100101 Firefox/110.0',
            },
        )
        days = response.json()['payload']['quota_type_maps'].get(
            'ConstantQuotaUsageDaily'
        )

        d = {}

        for date, status in days.items():
            d.update(
                {date: {'remaining': status['remaining'], 'total': status['total']}}
            )

        campsite.dates.update(d)

    campsites.update({campsite.division_id: campsite.to_dict()})

sys.stdout.write(json.dumps(campsites))
