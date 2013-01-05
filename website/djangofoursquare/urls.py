from django.conf.urls.defaults import *

from djangofoursquare.views import *

urlpatterns = patterns('djangofoursquare.views',    
    url(r'^auth/$',
        view=auth,
        name='foursquare_oauth_auth'),

    url(r'^return/$',
        view=return_,
        name='foursquare_oauth_return'),
    
    url(r'^clear/$',
        view=unauth,
        name='foursquare_oauth_unauth'),
)
