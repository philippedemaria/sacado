define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-question-flash_update-ace.js OK --");
 

            var code = $('#id_script').val(); 

            var editor = ace.edit("id_div_script");
            editor.getSession().setMode("ace/mode/python");
            editor.setValue(code);  
  
    });
});