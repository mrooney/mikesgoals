import oauth, httplib, time, datetime
from django.utils import simplejson

from django.http import *
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate

from django.contrib.auth.models import User
from utils import *

try:
    from djangodblog.middleware import DBLogMiddleware
except ImportError:
    class DBLogMiddleware(object):
        def process_exception(self, request, exception):
            pass

CONSUMER = oauth.OAuthConsumer(FOURSQUARE_CONSUMER_KEY, FOURSQUARE_CONSUMER_SECRET)
# CONNECTION = httplib.HTTPConnection(SERVER)

def get_consumer():
    return CONSUMER

def get_connection():
    # return CONNECTION
    return httplib.HTTPConnection(SERVER)

def unauth(request):
    request.session.clear()
    # request.session['notice'] = 'Logged out!'
    return HttpResponseRedirect('/?loggedout')

def auth(request):
    "/auth/"
    try:
        token = get_unauthorised_request_token(get_consumer(), get_connection())
        auth_url = get_authorisation_url(get_consumer(), token)
    except FoursquareError, e:
        DBLogMiddleware().process_exception(request, e)
        request.session['notice'] = "Sorry, the foursquare API rejected that request. No problem, try again!"
        return HttpResponseRedirect('/?error')
    
    request.session['unauthed_token'] = token.to_string()   
    return HttpResponseRedirect(auth_url)

def return_(request):
    "/return/"
    unauthed_token = request.session.get('unauthed_token', None)
    if not unauthed_token:
        request.session['notice'] = "Sorry, we couldn't properly process your authentication. Please try again, and let us know if it consistently fails."
        return HttpResponseRedirect('/?error')
    token = oauth.OAuthToken.from_string(unauthed_token)
    
    if token.key != request.GET.get('oauth_token', 'no-token'):
        request.session['notice'] = "Sorry, we couldn't log you in."
        return HttpResponseRedirect('/?error')
    
    try:
        access_token = exchange_request_token_for_access_token(
                get_consumer(), get_connection(), token)
    except (KeyError, FoursquareError), e:
        DBLogMiddleware().process_exception(request, e)
        request.session['notice'] = "Sorry, we experienced an error logging you in. Please try again."
        return HttpResponseRedirect('/?error')

    request.session['access_token'] = access_token.to_string()
        
    # Check if the token works on Twitter
    auth = is_authenticated(get_consumer(), get_connection(), access_token)
    if not auth:
        request.session['notice'] = "Sorry, you weren't authenticated by Foursquare."
        return HttpResponseRedirect('/?error')
        
    userdata = auth['user']
    
    try:
        user = authenticate(foursquare_user_data=userdata, 
                access_token=access_token.to_string())
    except FoursquareError, e:
        DBLogMiddleware().process_exception(request, e)
        request.session['notice'] = "Sorry, we experienced an error logging you in. Please try again."
        return HttpResponseRedirect('/?error')
        
    if user is None or not user.is_authenticated():
        request.session['notice'] = "Sorry, you weren't authenticated by Foursquare."
        return HttpResponseRedirect('/?error')
                        
    login(request, user)
    return HttpResponseRedirect('/')
        
