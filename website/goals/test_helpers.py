from django.utils import unittest
import django.test
from django.test.client import Client
from lxml import html, etree
from lxml.cssselect import CSSSelector

class NotOkay(Exception):
    def __init__(self, response):
        Exception.__init__(self, "%r: %r" % (response.status_code, response))
        self.response = response
        self.status = response.status_code

class ExtendedTestCase(django.test.TestCase):
    def after_setUp(self):
        """ Override this to do extra setup. """
    
    def before_tearDown(self):
        """ Override this to do extra tear-down. """
        
    def assertStatus(self, status, path, **kwargs):
        try:
            response = self.get(path, **kwargs)
        except NotOkay, no:
            response = no.response
            
        self.assertEqual(status, response.status_code)
        
    @classmethod
    def get_client(cls, user=None):
        client = Client()
        if user:
            client.login(username=user.username, password="foobar")
        return client
    
    @classmethod
    def _http_verb(cls, verb, path, client=None, data=None, https=False, user=None, **kwargs):
        data = data or {}
        client = client or cls.get_client(user)
        kwargs['HTTP_X_FORWARDED_PROTO'] = 'https' if https else 'http' # Simulates ELB
        response = getattr(client, verb.lower())(path, data=data, **kwargs)
        if response.status_code not in [200, 302]:
            raise NotOkay(response)
        return response

    @classmethod
    def get(cls, path, data=None, client=None, **kwargs):
        data = data or {}
        return cls._http_verb('get', path, client=client, **kwargs)

    @classmethod
    def post(cls, path, data=None, client=None, **kwargs):
        data = data or {}
        return cls._http_verb('post', path, data=data, client=client, **kwargs)

    @classmethod
    def _api_call(cls, path, data=None, client=None, method="post"):
        data = data or {}
        response = getattr(cls, method)(path,
                                        data=util.dumps(data),
                                        client=client,
                                        content_type="application/json")
        try:
            content = util.loads(response.content)
        except ValueError:
            # Probably not a JSON response, so just return a string.
            content = response.content
        return content

    @classmethod
    def api_post(cls, *args, **kwargs):
        return cls._api_call(*args, **kwargs)

    def parse_response(self, response):
        if isinstance(response, basestring):
            return html.fromstring(response)
        return html.fromstring(response.content)

    def css_select(self, response, css_selector):
        sel = css_selector if isinstance(css_selector, CSSSelector) else CSSSelector(css_selector)
        return [e for e in sel(self.parse_response(response))]

    def assertNumCssMatches(self, num, response, css_selector):
        found = len(self.css_select(response, css_selector))
        self.assertEqual(num, found, "Expected {0} but found {1}.".format(num, found))

