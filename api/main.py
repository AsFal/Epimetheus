from waitress import serve
from pyramid.config import Configurator
from pyramid.view import view_config, view_defaults
from pyramid.session import SignedCookieSessionFactory

from logs import TextLog, LogList, Entry


def api_start():

    my_session_factory = SignedCookieSessionFactory('itsaseekreet')
    with Configurator() as config:
        config.add_route('sessions', '/logs/sessions')
        config.add_route('report', '/logs/report')
        config.scan()
        config.set_session_factory(my_session_factory)
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
        GET -> Suggestions TODO: Need to implement suggestions to go by path
    /session
        /   GET -> Makes no sense to have this route
        /:user GET -> Makes no sense to have this route
        /start POST -> Start session with user's logs information
        /end DELETE -> End session for user
        /update PATCH -> Update the logs in a session for a user

Networking, make sure that this microservice only whitelists
pheonix ip for calls. No open to the general public.
'''

@view_config(request_method='GET', route_name='report', renderer='json')
def getReport(request):
    user = request.params["user"]
    entry = Entry(request.params["category"], request.params["name"])
    logList = users[user]
    return logList.getReport(entry)

'''
Very flawed piece of code below:
TODO: bust be changed for something more robust after  MVP
'''
users = {}

@view_defaults(route_name='sessions', renderer='json')
class SessionView(object):

    '''
    The current implementation of the sessions is based on the naive assumption that
    all of the containers will have access to the same memory. This is not necessarily true.

    TODO Q: Is there a way to use a common volume without the speed of a memory lookup
    '''
    def __init__(self, request):
        self.request = request
        self.user = request.params["user"]
        self.request.response.status = '200'

    def _addUserToSession(self, logs):
        users[self.user] = logs

    def _removeUserFromSession(self):
        del users[self.user]

    @view_config(request_method='POST')
    def startSession(self):
        textLogs = self.request.json_body
        logList = LogList(logs=[TextLog(logString).toTreeLog() for logString in textLogs])
        self._addUserToSession(logList)
        return users

    @view_config(request_method='DELETE')
    def endSession(self):
        self._removeUserFromSession()
        return self.request.session['users']

    @view_config(request_method='PUT')
    def updateUserLogs(self):
        return {}

