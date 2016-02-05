from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

@view_config(route_name='home')
def home(request):
    return HTTPFound(location='/app/')

@view_config(route_name='stats', renderer='json')
def stats(request):
    """ Just fake some numbers for now """
    from random import randint
    ac_variance = randint(-25, 25)
    pv_variance = randint(-30, 35)
    return {
        'ac_load': 500 + ac_variance,
        'ac_max_load': 1600, # FIXME hardcoded
        'pv_watt': 200 + pv_variance,
        'bat_watt': 500 + ac_variance - pv_variance
    }
