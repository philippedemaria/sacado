define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-question-flash_update-ace.js OK --");


        var editor = ace.edit("id_div_script");
        editor.setTheme("ace/theme/monokai");
        editor.session.setMode("ace/mode/python"); //        editor.session.setMode("ace/mode/python");
        editor.setOptions({
            'enableLiveAutocompletion': true,
            'highlightActiveLine': false,
            'highlightSelectedWord': true,
            'fontSize': '12pt',
        });
       


        var code = $('#id_script').val(); 

        var editor = ace.edit("id_div_script");
        editor.getSession().setMode("ace/mode/python");
        editor.setValue(code);  


        $('body').on('click', '#on_submit' , function (event) {
            var code = editor.getValue();   
            $('#id_script').val(code);    

         });
  

        CKEDITOR.replace('id_html', {
            height: '200px',
            width: '100%',
            toolbar:    
                [  
                    { name: 'clipboard', groups: [ 'clipboard', 'undo' ], items: [ 'Source', '-','Copy', 'Paste', 'PasteText' ] },
                    { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ], items: [ 'NumberedList', 'BulletedList', '-',   'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock' ] }, 
                    { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ], items: [ 'Bold', 'Italic', 'Underline'] },
                ] ,
        });


        

 




    });
});