var spinner = $("#spinner")

$(document)
  .ajaxStart(function () {
    spinner.show();
  })
  .ajaxStop(function () {
    spinner.hide();
  });