MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
)
 
INSTALLED_APPS = (
    'awikie'
)
 
ROOT_URLCONF = 'awikie.urls'
 
import os
ROOT_PATH = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    ROOT_PATH + '/templates',
)
