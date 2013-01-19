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

class BaseView(View):
    def get_page_title(self, path):
        return path if path else 'index'

    def get_protocol(self):
        return 'http' + ('s' if self.request.is_secure() else '')

    def get_base_url(self):
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
        page = Page.find(page_title)
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
        page = Page.find(attrs['page_title'])
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
            'current': Page.find(page_title),
        })
