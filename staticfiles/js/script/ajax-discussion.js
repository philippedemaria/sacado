define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-sendmail.js OK");

        $('#div_to_answer').hide();
        $('#answer_button').on('click', function () { 
                $('#div_to_answer').toggle(500);
            });

        $('#answer_close_button').on('click', function () { 
                $('#div_to_answer').toggle(500);
            });

 
        CKEDITOR.replace('texte', {
                height: '200px' ,
                toolbar:    
                    [  
                        { name: 'paragraph',  items: [ 'NumberedList', 'BulletedList', '-',   'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock' ] }, 
                        { name: 'basicstyles',  items: [ 'Bold', 'Italic', 'Underline',  ] },
                        { name: 'insert', items: ['Table', 'HorizontalRule', 'Smiley', 'SpecialChar']},
                    ] ,
            });





    });
});