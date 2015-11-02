from osm_users_site import site


class Serve(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start):
        environ['SCRIPT_NAME'] = '/osm_users_site'
        return self.app(environ, start)


application = Serve(site.app)
