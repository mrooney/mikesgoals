from coffin.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from goals import views

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.goals, name="home"),
    url(r'^totals/$', views.totals, name="totals"),
    url(r'^github/$', views.github, name="github"),

    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^signup/$', views.signup, name="signup"),

    # API
    url(r'^api/check$', views.api_check),
    url(r'^api/goal_edit$', views.api_goal_edit),
    url(r'^api/goal_new$', views.api_goal_new),
    url(r'^api/goal_delete$', views.api_goal_delete),

    url(r'', include('social_auth.urls')),
)
