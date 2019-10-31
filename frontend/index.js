import 'bulma/css/bulma.css'
import 'selectize/dist/css/selectize.css'
import './index.scss'

import $ from 'jquery'
import 'selectize'

$('select').selectize()

$('input[type=file]').on('change', function (event) {
  $(this).siblings('.file-name').html($(this).val().replace('C:\\fakepath\\', ''))
})

document.querySelector('body').addEventListener('click', function (event) {
  const el = event.target
  console.log({ el })
  if (el.matches('.favorite-star')) {
    const projectPk = el.dataset.projectPk
    fetch(`/projects/${projectPk}/favorite/`, {
      method: 'POST'
    }).then(res => {
      if (res.ok) {
        el.classList.toggle('fas')
        el.classList.toggle('far')
      }
    })
  }
})
