from django.contrib import admin
from tasklist.models import *

admin.site.register(Tasklist)
admin.site.register(Listitem)
admin.site.register(UserProfile)