from ib.bluelantern.event import ChargeMetricReceived, DischargeMetricReceived
from ib.bluelantern.interfaces import IEquipmentCache

def make_charge_handler(cache):
    def charge_handler(event):
        di = cache[event.instance][event.name]
        if 'current' in di and event.timestamp > di['lastseen']:
            if di['lastseen'] > 0:
                di['counter'] += (event.timestamp - di['lastseen']) * di['current']
            di['lastseen'] = event.timestamp
    return charge_handler

def init(config, cache):
    # initialise counter for each device
    for a in cache.values():
        for b in a.values():
            b['counter'] = 0
            b['lastseen'] = 0

    handler = make_charge_handler(cache)
    config.add_subscriber(handler, ChargeMetricReceived)
    config.add_subscriber(handler, DischargeMetricReceived)
