// File#: _0_required-label
(function() {
  document.querySelectorAll('label[for]:not([data-not-required])').forEach(function (elem) {
    var input = document.getElementById(elem.getAttribute('for'));
    console.log(input);
    if (input && input.required) {
      elem.innerHTML += '<span class="margin-left-xxxs color-accent">*</span>'
    }
  })
}());