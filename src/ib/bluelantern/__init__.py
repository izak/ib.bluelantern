import json
from collections import OrderedDict
from pyramid.config import Configurator
from ib.bluelantern.mqtt import mqtt_init
from ib.bluelantern.interfaces import IEquipmentCache

def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('home', '/')
    config.add_route('stats', '/stats')
    config.add_static_view('app', 'static/web/app', cache_max_age=3600)
    config.scan()

    # Read equipment file and set up cache
    equipment_file = config.registry.settings.get('equipment')
    if equipment_file is not None:
        equipment = json.load(open(equipment_file, 'r'))
    else:
        equipment = {}

    cache = OrderedDict(equipment)
    config.registry.registerUtility(cache, IEquipmentCache)

    # Set up MQTT link
    mqtt = mqtt_init(config, cache)
    mqtt.loop_start()

    return config.make_wsgi_app()
