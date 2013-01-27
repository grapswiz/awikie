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

fit = =>
  base_height = $('html').height() - $('header').height() - $('footer').height()
  $('#body').height base_height  - 100
  $('#edit_preview_area').height base_height - 70

$ =>
  body = $('#body')
  update_preview = => (
    (input, output) => output.html markdown.toHTML input.val()
  ) body, $('#preview_area')
  body.on 'input', => update_preview()
  update_preview()
  fit()

$(window).resize => fit()