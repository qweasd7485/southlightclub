$(document).ready(function() {

  $(document).on('change', '#selectFile', function() {
    var formData = new FormData();
    formData.append('fileToUpload',  $('#selectFile')[0].files[0]);
    formData.append('folderName',  '{{folderName}}');
    formData.append('csrfmiddlewaretoken',  "{{csrf_token}}");

    $.ajax({
      url: "{% url 'admin:upload' %}",
      type: 'POST',
      data: formData,
      cache: false,
      contentType: false,
      processData: false
    })
    .done(function(data) {
      var id = "[id^='mceu_'][id$='-inp']";
      $(id).attr({'value':data, 'disabled':true});
    })
    .fail(function() {
      alert('上傳失敗');
    });
  });
  
});
