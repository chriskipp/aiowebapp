$(document).ready(function() {
  $('.select2').select2({
    ajax: {
      url: '/completions',
      dataType: 'json'
    },
    placeholder: 'Search...',
    multiple: true,
    tokenSeparators: ' ',
  });
});

$('.select2').on('change', function(e) {
  var q = $('.select2').select2('data').map(x => x.text).join('+');

  if (q.length > 0) {
    $.ajax({
      url: '/search?q=' + q,
      success: function(result) {
  	    $('#result-list').loadTemplate(
          $('#search-result-template'),
          result
      )}
    })
  } else {
    return
  }
})
