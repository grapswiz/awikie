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

class Page(ndb.Model):
    title = ndb.StringProperty(required=True)
    body = ndb.TextProperty()
    updated_at = ndb.DateTimeProperty(required=True, auto_now=True)

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

    @classmethod
    def find_by_title(self, title):
        return Page.query().filter(Page.title == title).get()

    @classmethod
    def find_all(self):
        return Page.query().order(Page.title).fetch(1000)

class History(ndb.Model):
    title = ndb.StringProperty(required=True)
    body = ndb.TextProperty()
    updated_at = ndb.DateTimeProperty(required=True)

    @classmethod
    def find_by_title(self, title):
        q = History.query().filter(Page.title == title).order(-Page.updated_at)
        return q.fetch(100)

    @classmethod
    def find(self, key):
        return History.query().filter(Page.__key__ == Key(key)).get()

    def revert(self):
        Page(title=self.title, body=self.body).save()
