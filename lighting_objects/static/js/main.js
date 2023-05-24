$(function ($) {
$('#login-form').submit(function (e) {
        e.preventDefault()
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: 'json',
            success: function (response) {
                console.log('ok - ', response)
                if (response.status === 201) {
                    window.location.reload()
                } else if (response.status === 400) {
                    $('.alert-danger').text(response.error).removeClass('d-none')
                }
            },
            error: function (response) {
                console.log('err - ', response)
            }
        });
    });


  $('#details_modal').on('show.bs.modal', function (event) {
  let button = $(event.relatedTarget);
  let url = button.data('url');
  let container = $(this).find('.modal-body');
  container.html('');
  $.ajax({
    url: url,
  }).done(function(data){
    container.html(data);

  });
});

})

