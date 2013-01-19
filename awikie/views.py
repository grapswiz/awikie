# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context, loader

def index(request):
    return HttpResponse(loader.get_template('index.html').render(Context({})))
