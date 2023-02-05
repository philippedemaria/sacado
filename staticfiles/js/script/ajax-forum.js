define(['jquery', 'bootstrap', 'ui', 'ui_sortable','ckeditor'], function ($) {
    $(document).ready(function () { 
        console.log("chargement JS ajax-support_creator.js  OKK");


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

 
