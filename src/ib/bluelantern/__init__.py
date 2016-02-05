from pyramid.config import Configurator

def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_route('home', '/')
    config.add_route('stats', '/stats')
    config.add_static_view('app', 'static/web/app', cache_max_age=3600)
    config.scan()
    return config.make_wsgi_app()
