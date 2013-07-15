from coffin.conf.urls import *
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy

admin.autodiscover()

from goals import views

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^password_reset$', 'goals.views.password_reset', kwargs={'template_name': 'password_reset_form.jinja', 'post_reset_redirect': reverse_lazy('password_reset_done'), 'email_template_name': 'password_reset_email.html'}, name="password_reset"),
    url(r'^password_reset/done$', 'goals.views.password_reset_done', name="password_reset_done"),
    url(r'^reset(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', kwargs={'template_name': 'password_reset_confirm.html'}),
    url(r'^reset/done$', 'django.contrib.auth.views.password_reset_complete', kwargs={'template_name': 'password_reset_complete.html'}),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.goals, name="home"),
    url(r'^analytics/$', views.analytics, name="analytics"),
    url(r'^totals/$', views.totals, name="totals"),
    url(r'^github/$', views.github, name="github"),

    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^signup/$', views.signup, name="signup"),

    url(r'^command/$', views.command),

    # API
    url(r'^api/check$', views.api_check),
    url(r'^api/goal_edit$', views.api_goal_edit),
    url(r'^api/goal_new$', views.api_goal_new),
    url(r'^api/goal_delete$', views.api_goal_delete),

    url(r'', include('social_auth.urls')),
)
