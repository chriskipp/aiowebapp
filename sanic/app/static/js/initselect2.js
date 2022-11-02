$(document).ready(function() {
  $('.select2').select2({
    multiple: true,
    allowClear: true,
    placeholder: "Search...",
    tags: true,
    closeOnSelect: false,
    scrollAfterSelect: true ,
    tokenSeparators: ' ',
  })
  .val(null).trigger('change') // Clear Selection
});
