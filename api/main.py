from waitress import serve
from pyramid.config import Configurator
from pyramid.view import view_config, view_defaults

def api_start():
    with Configurator() as config:
        config.add_route('sessions', '/logs/sessions')
        config.scan()
        app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=6543)

'''
Api layout
I want this to be connected to the
logs and different functionlaities.

All of the routes take a
user id in the url params

Session is user,

logs/
    /analysis
        GET -> Gets all reports
        GET -> Nlp results
    /session
        /   GET -> Makes no sense to have this route
        /:user GET -> Makes no sense to have this route
        /start POST -> Start session with user's logs information
        /end DELETE -> End session for user
        /update PATCH -> Update the logs in a session for a user

Networking, make sure that this microservice only whitelists
pheonix ip for calls. No open to the general public.
'''

@view_defaults(route_name='sessions', renderer='json')
class SessionView(object):
    def __init__(self, request):
        self.request = request
        # self.user = request.params["user"]

    @view_config(
        request_method='POST',
        renderer='json'
    )
    def startSession(self):
        self.request.response.status = '200'
        return {'success': 'yass'}
