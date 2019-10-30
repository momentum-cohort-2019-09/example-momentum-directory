import 'bulma/css/bulma.css'
import 'selectize/dist/css/selectize.css'
import './index.scss'

import $ from 'jquery'
import 'selectize'

$('select').selectize()

$('input[type=file]').on('change', function (event) {
  $(this).siblings('.file-name').html($(this).val().replace('C:\\fakepath\\', ''))
})
