define(['jquery', 'bootstrap', 'ui', 'ui_sortable','ckeditor'], function ($) {
    $(document).ready(function () { 
        console.log("chargement JS writting-form.js");


        CKEDITOR.replace('answer', {
                height: '600px' ,
                width:'100%',
                toolbar:    
                    [  
                        { name: 'paragraph',  items: [ 'Preview','Print','-','NumberedList', 'BulletedList', '-',   'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock' ] }, 
                        { name: 'basicstyles',  items: [ 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript','-','TextColor', 'BGColor' ] },
                        { name: 'insert', items: [ 'Image','Table', 'HorizontalRule', 'Smiley', 'SpecialChar','Iframe']},                        
                        {name: 'styles', items: ['Format', 'Font', 'FontSize']},


                    ] ,
            });

});

});

 
 