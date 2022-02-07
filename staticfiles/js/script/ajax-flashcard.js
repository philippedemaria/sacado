define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-flashcard.js OK + cke");


/*enterMode: CKEDITOR.ENTER_BR, 
    toolbar:    
[   { name: 'document', groups: [ 'document', 'doctools' ], items: [ 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates' ] },
    { name: 'clipboard', groups: [ 'clipboard', 'undo' ], items: [ 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo' ] },
    { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ], items: [ 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl' ] },        '/',
    { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ], items: [ 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat' ] },
    { name: 'links', items: [ 'Link', 'Unlink', 'Anchor' ] }, { name: 'editing', groups: [ 'find', 'selection', 'spellchecker' ], items: [ 'Find', 'Replace', '-', 'SelectAll', '-', 'Scayt' ] },
    { name: 'insert', items: [ 'Image', 'Table', 'HorizontalRule', 'SpecialChar', 'PageBreak', 'Iframe', 'Syntaxhighlight' ] }, '/',
    { name: 'styles', items: [ 'Format', 'Font', 'FontSize' ] },
    { name: 'colors', items: [ 'TextColor', 'BGColor' ] },
    { name: 'others', groups: [ 'mode' ], items: [ 'Source', 'searchCode', 'autoFormat', 'CommentSelectedRange', 'UncommentSelectedRange', 'AutoComplete', '-', 'ShowBlocks' ] },
    { name: 'tools', items: [ 'Maximize' ] },
]
*/

        CKEDITOR.replace( 'id_question', {     
            height: 300,              
            width: 600,
            toolbarCanCollapse : false,                  
            allowedContent: true,   
            enterMode: CKEDITOR.ENTER_BR, 
            toolbar:    
            [  
                { name: 'insert', items: [ 'Image', ] }, 
                { name: 'styles', items: [ 'FontSize' ] },
                { name: 'paragraph', groups: [ 'list', 'align' ], items: [ 'NumberedList', 'BulletedList', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',] },
                { name: 'others', groups: [ 'mode' ], items: [ 'Source'] },
            ]

            } );


        CKEDITOR.replace( 'id_answer', {     
            height: 300,              
            width: 600,
            toolbarCanCollapse : false,                  
            allowedContent: true,   
            enterMode: CKEDITOR.ENTER_BR, 
            toolbar:    
            [  
                { name: 'insert', items: [ 'Image', ] }, 
                { name: 'styles', items: [ 'FontSize' ] },
                { name: 'paragraph', groups: [ 'list', 'align' ], items: [ 'NumberedList', 'BulletedList', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',] },
                { name: 'others', groups: [ 'mode' ], items: [ 'Source'] },
            ]

            } );

        CKEDITOR.replace( 'id_helper', {     
            height: 300,              
            width: 600,
            toolbarCanCollapse : false,                  
            allowedContent: true,   
            enterMode: CKEDITOR.ENTER_BR, 
            toolbar:    
            [  
                { name: 'insert', items: [ 'Image', ] }, 
                { name: 'styles', items: [ 'FontSize' ] },
                { name: 'paragraph', groups: [ 'list', 'align' ], items: [ 'NumberedList', 'BulletedList', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',] },  
                { name: 'others', groups: [ 'mode' ], items: [ 'Source'] },
            ]

            } );


        $("#this_question_textarea_display").click(function(){ 
            var value = CKEDITOR.instances['id_question'].getData(); 
            $('#type_of_textarea_display').html("la question");
            $('#body_of_textarea_display').html(value);
            $('#body_of_textarea_display').addClass("qflashcard").removeClass("hflashcard").removeClass("aflashcard");
            MathJax.Hub.Queue(['Typeset',MathJax.Hub,'body_of_textarea_display']); 
        });


        $("#this_answer_textarea_display").click(function(){             
            var value = CKEDITOR.instances['id_answer'].getData();
            $('#type_of_textarea_display').html("la réponse");
            $('#body_of_textarea_display').html(value);
            $('#body_of_textarea_display').addClass("aflashcard").removeClass("hflashcard").removeClass("qflashcard");
            MathJax.Hub.Queue(['Typeset',MathJax.Hub,'body_of_textarea_display']); 
        });

        
        $("#this_helper_textarea_display").click(function(){ 
            var value = CKEDITOR.instances['id_helper'].getData();
            $('#type_of_textarea_display').html("l'aide");
            $('#body_of_textarea_display').html(value);
            $('#body_of_textarea_display').addClass("hflashcard").removeClass("qflashcard").removeClass("aflashcard");
            MathJax.Hub.Queue(['Typeset',MathJax.Hub,'body_of_textarea_display']); 

        });




});

});

