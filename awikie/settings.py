# -*- coding: utf-8 -*-

#    awikie -- This is Wiki engine working in Google App Engine.
#    Copyright (C) <2013> Motoki Naruse <motoki@naru.se>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

CACHE_BACKEND = 'memcached:///'

import sys
sys.path.append(ROOT_PATH + '/lib')

AUTHORIZED_USER = (

)
