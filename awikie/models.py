# -*- coding: utf-8 -*-
from google.appengine.ext import db

class Page(db.model):
    title = db.StringProperty(require=True)
    body = db.TextProperty()
    updated_at = db.DateTimeProperty(required=True)

class History(db.model):
    title = db.StringProperty(require=True)
    body = db.TextProperty()
    updated_at = db.DateTimeProperty(required=True)

