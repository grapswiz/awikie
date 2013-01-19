###
    awikie -- This is Wiki engine working in Google App Engine.
    Copyright (C) <2013> Motoki Naruse <motoki@naru.se>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###

$ =>
  form = $('#history_form')
  preview_area = $('#preview_area')
  page_title = $('#page_title').html()
  current = $('#current')

  preview = (item) =>
    key = item.data 'key'
    if key is page_title
      form.attr 'action', key
      form.attr 'method', 'get'
    else
      form.attr 'action', 'history/' + key
      form.attr 'method', 'post'
    preview_area.html markdown.toHTML $('#' + key).html()

  current.on 'click', => preview current
  $('.preview').each -> ((item) => item.on 'click', => preview item) $(this)

  preview current