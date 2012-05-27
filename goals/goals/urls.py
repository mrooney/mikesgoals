from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from goals import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'goals.views.home', name='home'),
    # url(r'^goals/', include('goals.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.goals, name="home"),

    # API
    url(r'^api/check$', views.api_check),
)
