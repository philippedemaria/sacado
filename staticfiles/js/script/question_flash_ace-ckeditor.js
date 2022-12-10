define(['jquery', 'bootstrap', 'ckeditor'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-question-flash_ace-ckeditor.js OK --");


        
        var editor = ace.edit("id_div_script");
        editor.setTheme("ace/theme/monokai");
        editor.session.setMode("ace/mode/python"); //        editor.session.setMode("ace/mode/python");
        editor.setOptions({
            'enableLiveAutocompletion': true,
            'highlightActiveLine': false,
            'highlightSelectedWord': true,
            'fontSize': '12pt',
        });
       
        code = 'n = randint(0,9)\ntitle = ""  \nanswer =   \nwans =  ""  '
        editor.setValue(code); 


        $('body').on('click', '#on_submit' , function (event) {
            var code = editor.getValue();   
            $('#id_script').val(code);    

         });

        //
        // 
        // Donne la forme de wans 
        //
        //        
        // $('body').on('blur', '#id_html' , function (event) {

        //     var myString = CKEDITOR.instances['html'].getData();

        //     alert(myString) ; 

        //     if ( myString.indexOf('input') > -1 ){

        //         var idx = myString.indexOf('input')+6;
        //         var newString = myString.substring(idx,myString.indexOf(']'));
        //         var code_html = "Voici une aide à la déclaration de variable à mettre dans le code Python :\n\n"+ newString + "=......_##_" ;

        //         alert(code_html); 

        //     }
        //  });



    
        CKEDITOR.replace('id_html', {
            height: '200px',
            width: '100%',
            toolbar:    
                [  
                    { name: 'clipboard', groups: [ 'clipboard', 'undo' ], items: [ 'Source', '-','Copy', 'Paste', 'PasteText' ] },
                    { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ], items: [ 'NumberedList', 'BulletedList', '-',   'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock' ] }, 
                    { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ], items: [ 'Bold', 'Italic', 'Underline', 'FontSize'] },
                ] ,
        });

    });
});