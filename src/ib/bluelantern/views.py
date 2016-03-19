from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from ib.bluelantern.interfaces import IEquipmentCache

@view_config(route_name='home')
def home(request):
    return HTTPFound(location='/app/')

@view_config(route_name='stats', renderer='json')
def stats(request):
    cache = request.registry.getUtility(IEquipmentCache)
    ac_load = ac_max_load = pv_watt = pv_max_watt = bat_watt = 0.0
    for instance, a in cache.items():
        has_bmv = False # Assume no BMV until you find one
        instance_pv = instance_load = instance_bat = 0

        for id, b in a.items():
            t = b.get('type', None)
            if t == 'pv':
                instance_pv += float(b.get('power', 0))
                pv_max_watt += float(b.get('max_power', 0))
            elif t == 'load':
                instance_load += float(b.get('power', 0))
                ac_max_load += float(b.get('max_power', 0))
            elif t == 'monitor':
                has_bmv = True
                instance_bat += float(b.get('power', 0))

        if has_bmv:
            # Estimate PV watts as load plus whatever makes it into the
            # battery. This uses the more accurate BMV number and takes
            # inefficiencies from the PV figure.
            ac_load += instance_load
            pv_watt += (instance_load + instance_bat)
        else:
            # No BMV. Estimate battery delta as difference between
            # charge and load
            ac_load += instance_load
            pv_watt += instance_pv
            instance_bat += (instance_pv - instance_load)

        bat_watt += instance_bat

    return {
        'ac_load': ac_load,
        'ac_max_load': ac_max_load,
        'pv_watt': pv_watt,
        'pv_max_watt': pv_max_watt,
        'bat_watt': bat_watt,
    }
