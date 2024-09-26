destination_ids=4675321

.INTERMEDIATE : data/notifications.json data/finished/backcountry_sites.json data/intermediate/backcountry_sites.json

notify : data/notifications.json
	python -m backcountry.notify $<
	cp $< data/finished/notifications-$(shell date +%s).json

data/notifications.json : data/finished/backcountry_sites.json
	python -m backcountry.subscriptions $< > $@

data/finished/backcountry_sites.json : data/intermediate/backcountry_sites.json
	python -m backcountry.get_site_availability $< > $@

data/intermediate/backcountry_sites.json :
	python backcountry/get_backcountry_sites.py > $@
