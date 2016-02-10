from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from ib.bluelantern.interfaces import IEquipmentCache

@view_config(route_name='home')
def home(request):
    return HTTPFound(location='/app/')

@view_config(route_name='stats', renderer='json')
def stats(request):
    cache = request.registry.getUtility(IEquipmentCache)
    # TODO, add up values in cache and use that instead.
    if cache:
        ac_load = ac_max_load = pv_watt = pv_max_watt = bat_watt = 0.0
        for instance, a in cache.items():
            for id, b in a.items():
                t = b.get('type', None)
                if t == 'pv':
                    pv_watt += float(b.get('power', 0))
                    pv_max_watt += float(b.get('max_power', 0))
                elif t == 'load':
                    ac_load += float(b.get('power', 0))
                    ac_max_load += float(b.get('max_power', 0))
        bat_watt = pv_watt - ac_load
        return {
            'ac_load': ac_load,
            'ac_max_load': ac_max_load,
            'pv_watt': pv_watt,
            'pv_max_watt': pv_max_watt,
            'bat_watt': bat_watt,
        }
    else:
        """ Just fake some numbers for now """
        from random import randint
        ac_variance = randint(-25, 25)
        pv_variance = randint(-30, 35)
        return {
            'ac_load': 500 + ac_variance,
            'ac_max_load': 1600,
            'pv_watt': 200 + pv_variance,
            'pv_max_watt': 1000,
            'bat_watt': 500 + ac_variance - pv_variance
        }
