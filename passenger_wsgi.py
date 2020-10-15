import sacado.wsgi
SCRIPT_NAME = '/home/c1398844c/sacado'

class PassengerPathInfoFix(object):
    """
    Sets PATH_INFO from REQUEST_URI because Passenger doesn't provide it.
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        from urllib.parse import unquote
        environ['SCRIPT_NAME'] = SCRIPT_NAME
        try :
            request_uri = unquote(environ['REQUEST_URI'])
            script_name = unquote(environ.get('SCRIPT_NAME', ''))
            offset = request_uri.startswith(script_name) and len(environ['SCRIPT_NAME']) or 0
            environ['PATH_INFO'] = request_uri[offset:].split('?', 1)[0]
            return self.app(environ, start_response)
        except :
            return self.app(environ, start_response)



application = sacado.wsgi.application
application = PassengerPathInfoFix(application)
