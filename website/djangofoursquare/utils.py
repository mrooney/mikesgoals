import oauth
import time
import httplib
from django.conf import settings

from django.utils import simplejson

signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

SERVER = getattr(settings, 'OAUTH_SERVER', 'foursquare.com')
REQUEST_TOKEN_URL = getattr(settings, 'OAUTH_REQUEST_TOKEN_URL', 'http://%s/oauth/request_token' % SERVER)
ACCESS_TOKEN_URL = getattr(settings, 'OAUTH_ACCESS_TOKEN_URL', 'http://%s/oauth/access_token' % SERVER)
AUTHORIZATION_URL = getattr(settings, 'OAUTH_AUTHORIZATION_URL', 'http://%s/oauth/authorize' % SERVER)

FOURSQUARE_CONSUMER_KEY = getattr(settings, 'FOURSQUARE_CONSUMER_KEY', 'YOUR_KEY')
FOURSQUARE_CONSUMER_SECRET = getattr(settings, 'FOURSQUARE_CONSUMER_SECRET', 'YOUR_SECRET')

FOURSQUARE_API_USER_AGENT = getattr(settings, 'FOURSQUARE_API_USER_AGENT', 'Django-Foursquare-App')

class FoursquareError(IOError): pass

def request_oauth_resource(consumer, url, access_token, parameters=None, 
        signature_method=signature_method, http_method='POST'):
    """
    usage: request_oauth_resource( consumer, '/url/', your_access_token, parameters=dict() )
    Returns a OAuthRequest object
    """
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, token=access_token, http_url=url, parameters=parameters,
        http_method=http_method
    )
    oauth_request.sign_request(signature_method, consumer, access_token)
    return oauth_request


def fetch_response(oauth_request, connection):
    url = oauth_request.to_url()
    headers = {
        'User-Agent': FOURSQUARE_API_USER_AGENT
    }
    
    total_tries = 3
    tries_remaining = total_tries
    while tries_remaining:
        try:
            connection.request(oauth_request.http_method, url, headers=headers)
            break
        except httplib.socket.error:
            raise FoursquareError("Error connecting to Foursquare")
        except httplib.CannotSendRequest:
            try:
                discard = connection.getresponse()
            except httplib.BadStatusLine:
                pass
            
            tries_remaining -= 1
            if tries_remaining:
                time.sleep(0.25)
                continue
            else:
                raise FoursquareError("Cannot send request after %d tries." % total_tries)
    
    try:
        response = connection.getresponse()
    except httplib.BadStatusLine, e:
        raise FoursquareError("Bad status line.")
    
    if response.status != 200:
        raise FoursquareError('Response to foursquare call yielded status \
code %s: data: %s' % (response.status, response.read()))

    s = response.read()
    return s

def get_unauthorised_request_token(consumer, connection, signature_method=signature_method):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, http_url=REQUEST_TOKEN_URL
    )
    oauth_request.sign_request(signature_method, consumer, None)
    resp = fetch_response(oauth_request, connection)
    try:
        token = oauth.OAuthToken.from_string(resp)
    except KeyError:
        raise FoursquareError('Response from foursquare call\
yielded invalid unauthorized request token %s' % resp)
    return token


def get_authorisation_url(consumer, token, signature_method=signature_method):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, token=token, http_url=AUTHORIZATION_URL
    )
    oauth_request.sign_request(signature_method, consumer, token)
    return oauth_request.to_url()

def exchange_request_token_for_access_token(consumer, connection, request_token, signature_method=signature_method):
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(
        consumer, token=request_token, http_url=ACCESS_TOKEN_URL
    )
    oauth_request.sign_request(signature_method, consumer, request_token)
    resp = fetch_response(oauth_request, connection)
    return oauth.OAuthToken.from_string(resp) 

def is_authenticated(consumer, connection, access_token):
    
    oauth_request = request_oauth_resource(consumer, 
            'http://api.foursquare.com/v1/user.json', access_token,
            http_method='GET')
    try:
        json = fetch_response(oauth_request, connection)
    except Exception, e:
        raise FoursquareError('%s: %s' % (e.__class__.__name__, str(e)))

    if 'id' in json:
        return simplejson.loads(json)
    return False

def make_request(consumer, connection, access_token, url, method='GET', **kwargs):

    oauth_request = request_oauth_resource(consumer, url, 
            access_token, http_method=method,
            parameters=kwargs)
    try:
        json = fetch_response(oauth_request, connection)
    except Exception, e:
        raise FoursquareError('%s: %s' % (e.__class__.__name__, str(e)))
        
    return simplejson.loads(json)
    
def get_user(consumer, connection, access_token, uid):
    return make_request(consumer, connection, access_token, 
            'http://api.foursquare.com/v1/user.json', uid=uid)

def get_checkins(consumer, connection, access_token):
    return make_request(consumer, connection, access_token, 
            'http://api.foursquare.com/v1/checkins.json')

def send_friend_request(consumer, connection, access_token, uid):
    return make_request(consumer, connection, access_token, 
            'http://api.foursquare.com/v1/friend/sendrequest.json', method='POST',
            uid=uid)

def approve_friend_request(consumer, connection, access_token, uid):
    return make_request(consumer, connection, access_token, 
            'http://api.foursquare.com/v1/friend/approve.json', method='POST',
            uid=uid)