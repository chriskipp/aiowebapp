function collapseSidebar() {
  $('#sidebar_collapse').toggle();
  if (typeof SlickGrid.gridObjects.resizer != undefined) {
    SlickGrid.gridObjects.resizer.resizeGrid();
  }
  if (typeof map != undefined) {
    var m = map.invalidateSize();
  }
}

function getVal() {
  return (this.value)
}

$('#loginModal').on('shown.bs.modal', function () {
  $('#loginField').trigger('focus')
})
