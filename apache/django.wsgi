import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'listico.settings'

sys.path.append("/var/www")
sys.path.append("/var/www/listico/")
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
