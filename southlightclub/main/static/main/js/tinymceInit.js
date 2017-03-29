$(document).ready(function() {
  
  $('#selectFile').hide();
  tinymce.init({
    selector: 'textarea',  
    language: 'zh_TW',
    fontsize_formats: '8pt 10pt 12pt 14pt 16pt 18pt 20pt 22pt 24pt 26pt 36pt 48pt 62pt 70pt',
    theme: 'modern',
    width: '90%',
    height: '200px', 
    plugins: [
      'advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker',
      'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
      'save table contextmenu directionality emoticons template paste textcolor'
    ],
    // content_css: 'css/content.css',
    toolbar: 'insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media fullpage | forecolor backcolor emoticons | fontselect | fontsizeselect',
    setup: function(ed) {
      ed.on('init', function() {
        this.getDoc().body.style.fontSize = '12px'; // 字體預設大小
      });
    },
    file_browser_callback: function(field_name, url, type, win) {
      if(type=='image') {
        $('#selectFile').val('');
        $('#selectFile').click();
      }
    }
  });

});