$ =>
  body = $('#body')
  update_preview = => (
    (input, output) => output.html markdown.toHTML input.val()
  ) body, $('#preview_area')
  body.on 'input', => update_preview()
  update_preview()
