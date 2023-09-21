define(['jquery', 'bootstrap', 'ui', 'ui_sortable','ckeditor'], function ($) {
    $(document).ready(function () { 
        console.log("chargement JS bibliotex_from_tex.js  OKK");



        //**************************************************************************************************************
        //********            ckEditor            **********************************************************************
        //**************************************************************************************************************
        var nb = $(".ckeditor_class").length ;

        for(var i=0;i<nb;i++)
        {

            CKEDITOR.replace('eno'+i, {
                    height: '250px',
                    filebrowserBrowseUrl : '/ckeditor/browse/',
                    filebrowserUploadUrl : '/ckeditor/upload/',  
                    toolbar:    
                        [  
                            { name: 'paragraph', items: [ 'NumberedList', 'BulletedList', '-',   'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock' ] }, 
                            { name: 'basicstyles',  items: [ 'Bold', 'Italic', 'Underline',  ] },
                            { name: 'insert', items: ['Image', 'SpecialChar','Iframe']},   
                            { name: 'styles', items : [ 'Styles', 'TextColor','BGColor' ] },
                        ] ,
                });

            CKEDITOR.replace('cor'+i, {
                height: '250px',
                filebrowserBrowseUrl : '/ckeditor/browse/',
                filebrowserUploadUrl : '/ckeditor/upload/',  
                toolbar:    
                    [  
                        { name: 'paragraph', items: [ 'NumberedList', 'BulletedList', '-',   'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock' ] }, 
                        { name: 'basicstyles',  items: [ 'Bold', 'Italic', 'Underline',  ] },
                        { name: 'insert', items: ['Image', 'SpecialChar','Iframe']},   
                        { name: 'styles', items : [ 'Styles', 'TextColor','BGColor' ] },
                    ] ,
            });


        }

 



 

});

});

 
