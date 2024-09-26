import json
import sys

with open('data/subscriptions.json') as f:
    subscriptions = json.load(f)

with open('data/finished/backcountry_sites.json') as f:
    sites = json.load(f)

notify = {}


for email, subscription in subscriptions.items():
    # subscription = Subscription(email=email, dates=s['dates'], campsite=sites.get(s['site_id'])
    notify.update({email: {}})

    for id, subscription_dates in subscription['sites'].items():
        site = sites.get(id)

        for date, status in subscription_dates['dates'].items():
            current = site['dates'].get(date)

            sub_date = subscription_dates['dates'].get(date)

            if not current:
                continue

            if not sub_date:
                if current['remaining'] > 0:
                    try:
                        notify[email][site['name']].update({date: current})
                    except KeyError:
                        notify[email].update({site['name']: {date: current}})
            elif sub_date.get('remaining') != current['remaining']:
                if current['remaining'] > 0:
                    try:
                        notify[email][site['name']].update({date: current})
                    except KeyError:
                        notify[email].update({site['name']: {date: current}})

            subscription['sites'][id]['dates'].update({date: current})

    if notify[email] == {}:
        del notify[email]

with open('data/subscriptions.json', 'w') as f:
    json.dump(subscriptions, f)

sys.stdout.write(json.dumps(notify))
