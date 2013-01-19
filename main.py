import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'awikie.settings'

import django.core.handlers.wsgi
app = django.core.handlers.wsgi.WSGIHandler()
