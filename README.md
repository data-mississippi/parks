# parks

A lightweight data pipeline that sends email notifications to subscribers whenever a reservation opens up at their favorite Glacier National Park backcountry campsite. The pipeline is orchestrated by a Makefile that is setup to run automatically as a Github Action.

### Scripts overview
1. Manually add new subscribers with `backcountry/add_user.py`, passing arguments with their preferred campsites and dates.
2. `backcountry/get_backcountry_sites.py` gets a list of valid campsites and dumps it into a file.
3. `backcountry/get_site_availability.py` downloads the availability of each campsite.
4. `backcountry/subscriptions.py` checks to see if any of the subscribers' chosen campsites have a reservation opening on their preferred dates.
5. `backcountry/notify.py` notifies subscribers if there was an opening.

Thank you robot! Time to go outside!
