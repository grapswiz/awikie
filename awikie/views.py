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

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.views.generic import View
from models import *
import markdown
from django.conf import settings
from google.appengine.api import users

class BaseView(View):
    def dispatch(self, request, *args, **kwargs):
        # Authentication
        if not users.get_current_user().email() in settings.AUTHORIZED_USER:
            if not 'localhost' == request.META['SERVER_NAME']:
                if not 0 == len(settings.AUTHORIZED_USER):
                    return HttpResponse(status=403)
        return View.dispatch(self, request, *args, **kwargs)

    def get_page_title(self, path):
        """Return path. if empty, index."""
        return path if path else 'index'

    def get_protocol(self):
        """Return protcol used to request from client."""
        return 'http' + ('s' if self.request.is_secure() else '')

    def get_base_url(self):
        """Return URL in 'http://hostname:port' or'https://hostname:port'
        format"""
        return '{protocol}://{host}'.format(
            protocol=self.get_protocol(),
            host=self.request.get_host(),
        )

    def http_response(self, template, attrs={}):
        attrs['base_url'] = self.get_base_url()
        return HttpResponse(loader.get_template(template).render(Context(attrs)))

    def http_redirect(self, path):
        return HttpResponseRedirect(self.get_base_url() + '/' + path)

class BrowserView(BaseView):
    def get(self, request, path):
        page_title = self.get_page_title(path)
        page = Page.find_by_title(page_title)
        if page:
            return self.http_response('index.html', {
                'page_title': page_title,
                'body': markdown.Markdown().convert(page.body),
            })
        else:
            return self.http_redirect('edit/' + page_title)

class EditView(BaseView):
    def get(self, request, path):
        attrs = {
            'page_title': self.get_page_title(path),
        }
        page = Page.find_by_title(attrs['page_title'])
        if page:
            attrs['body'] = page.body
        return self.http_response('edit.html', attrs)

    def post(self, request, path):
        page_title = self.get_page_title(path)
        Page(title=page_title, body=request.POST['body']).save()

        return self.http_redirect(page_title)

class HistoryView(BaseView):
    def get(self, request, path):
        page_title = self.get_page_title(path)

        return self.http_response('history.html', {
            'page_title': page_title,
            'histories': History.find_by_title(page_title),
            'current': Page.find_by_title(page_title),
        })

    def post(self, request, path):
        history = History.find(path)
        if history:
            path = history.title
            history.revert()
        return self.http_redirect(path)

class PageListView(BaseView):
    def get(self, request):
        return self.http_response('page_list.html', {
            'page_list': Page.find_all()
        })
