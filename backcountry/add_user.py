from datetime import datetime
import json
import argparse

# Set up the argument parser
parser = argparse.ArgumentParser(
    description='Add a user to a list of backcountry sites.'
)
parser.add_argument('--email', type=str, help='The user\'s email address')
parser.add_argument(
    '--sites',
    type=str,
    help='The list of sites the user is registered for, separated by commas',
)
parser.add_argument(
    '--dates',
    type=str,
    help='The dates the user is registered for, separated by commas',
)

# Parse the arguments
args = parser.parse_args()

email = args.email
sites = args.sites.split(',')
dates = [
    datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
    for date_str in args.dates.split(',')
]

with open('data/admin/backcountry_sites.json', 'r') as f:
    sites_map = json.load(f)

new_subscription = {email: {'sites': {}}}

for id, site in sites_map.items():

    if site['campsite'] in sites:
        if id not in new_subscription[email]:
            new_subscription[email]['sites'][id] = {'dates': {}}

            for date in dates:
                if date not in new_subscription[email]['sites'][id]['dates']:
                    new_subscription[email]['sites'][id]['dates'][date] = {}

subscriptions_file = 'data/subscriptions.json'
with open(subscriptions_file, 'r') as f:
    subscriptions = json.load(f)

subscriptions.update(new_subscription)

with open(subscriptions_file, 'w') as f:
    json.dump(subscriptions, f, indent=4)
