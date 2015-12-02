''' Provided '''
import sys, SocketServer 
from bottle import route, run, template, redirect, request
import ece568helper

@route('/hello')
def hello():
    print 'hello invoked'
    return "Hello World!"

''' Implement Here '''

login_scope = 'profile'
email_scope = 'email'

@route('/login.html')
def login():
    return ece568helper.get_login_html(_addr, _port, _cid, login_scope, email_scope)

@route('/auth.html')
def auth():
    return ece568helper.get_auth_html(_cid)

import oauth2client
from oauth2client import client
import json
import apiclient
from apiclient.discovery import build
from apiclient import errors
import httplib2

SCOPES = [
    'https://www.googleapis.com/auth/drive.appfolder'
]

@route('/drive.html')
def drive():
    # Initialize client object to use Google api.
    # You need client_secrets.json downloaded and stored
    # in the current working directory 
    flow = ece568helper.get_client_object(_addr, _port, SCOPES)
    auth_uri = flow.step1_get_authorize_url()
    params = dict(request.params)
    
    if not params or not params['code']:
        redirect(auth_uri)
        return template('drive', result='fail') 

    auth_code = params['code']
    credentials = flow.step2_exchange(auth_code)
    # http_auth = credentials.authorize(httplib2.Http())

    ece568helper.output_helper('credentials', credentials)

    # TODO - upload
    return template('drive', result='fail')



''' Provided '''

try:
    _addr = sys.argv[1]
    _port = sys.argv[2]
    _cid = sys.argv[3]
    run(host=_addr, port=_port, debug=True)
except IndexError:
    print 'Usage: python ece568app.py <IP address> <Port> <Client ID>'
except SocketServer.socket.error:
    print '[Fail] port ' + str(_port) + ' is already in use\n' 

