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

from google.appengine.ext import ndb
from google.appengine.api.datastore import Key
from django.core.cache import cache
import base64

class Page(ndb.Model):
    title = ndb.StringProperty(required=True)
    body = ndb.TextProperty()
    updated_at = ndb.DateTimeProperty(required=True, auto_now=True)

    @classmethod
    def b64encode(self, source):
        return base64.b64encode(source.encode('utf-8'))

    @classmethod
    def get_cache_name(self, title):
        return 'Page_' + Page.b64encode(title)

    @classmethod
    def get_list_cache_name(self):
        return 'Page_list'

    def save(self):
        old = Page.query().filter(Page.title == self.title).get()
        if old:
            History(
                title=old.title,
                body=old.body,
                updated_at=old.updated_at
            ).put()
            old.body = self.body
            self = old
        self.put()
        cache.set(Page.get_cache_name(self.title), self, 86400)
        cache.delete(Page.get_list_cache_name())

    @classmethod
    def find_by_title(self, title):
        cache_name = Page.get_cache_name(title)
        cached = cache.get(cache_name)
        if cached:
            return cached
        page = Page.query().filter(Page.title == title).get()
        cache.set(cache_name, page, 86400)

        return page

    @classmethod
    def find_all(self):
        list_cache_name = Page.get_list_cache_name()
        cached = cache.get(list_cache_name)
        if cached:
            return cached
        page_list = Page.query().order(Page.title).fetch(1000)
        cache.set(list_cache_name, page_list, 86400)

        return page_list

class History(ndb.Model):
    title = ndb.StringProperty(required=True)
    body = ndb.TextProperty()
    updated_at = ndb.DateTimeProperty(required=True)

    @classmethod
    def find_by_title(self, title):
        q = History.query().filter(History.title == title).order(-History.updated_at)
        return q.fetch(100)

    @classmethod
    def find(self, key):
        return History.query().filter(History.__key__ == Key(key)).get()

    def revert(self):
        Page(title=self.title, body=self.body).save()
