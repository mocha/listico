from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from tasklist.views import *

# Insert email_login overrides
from email_login import useradmin, adminsite
site = adminsite.EmailLoginAdminSite()
# duplicate the normal admin's registry until ticket #8500 get's fixed
site._registry = admin.site._registry

urlpatterns = patterns('',

  (r'^admin/', include(site.urls)),
  (r'^accounts/', include('email_login.urls')),
  
  (r'^$', homepage),

  (r'^list/(?P<list_id>\d*)/$', list_page),
  (r'^list/new$', new_list),

  (r'^list/(?P<list_id>\d*)/add_task$', add_task),
  (r'^list/(?P<list_id>\d*)/delete$', delete_list),

  (r'^complete_task/(?P<task_id>\d*)/$', complete_task),
  (r'^uncomplete_task/(?P<task_id>\d*)/$', uncomplete_task),
  (r'^delete_task/(?P<task_id>\d*)/$', delete_task),
  (r'^undelete_task/(?P<task_id>\d*)/$', undelete_task),


  (r'^signup/$', signup),

  # auth.views
  (r'^register/$', signup),
  (r'^account/', include('email_login.urls')),
  (r'^logout/$', logout_page),
  (r'^password_change/$', 'django.contrib.auth.views.password_change'),
  (r'^password_change/done/$', 'django.contrib.auth.views.password_change_done'),
  (r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
  (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
  (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
  (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),

)
