define(['jquery', 'ckeditor', 'ckeditor_jquery'], function ($) {
    console.log("config0");
    $(document).ready(function () {
 
        var enonce = CKEDITOR.instances.enonce;
        console.log(enonce);
        if (enonce) {
            enonce.destroy(true);
        }

        CKEDITOR.replace('enonce', {
            filebrowserBrowseUrl: './plugins/ckfinder/ckfinder.html',
            filebrowserImageBrowseUrl: './plugins/ckfinder/ckfinder.html?type=Images',
            filebrowserUploadUrl: './plugins/ckfinder/core/connector/php/connector.php?command=QuickUpload&type=Files',
            filebrowserImageUploadUrl: './plugins/ckfinder/core/connector/php/connector.php?command=QuickUpload&type=Images'
        });


CKEDITOR.on("instanceReady", function(e) {
 var $frame = $(e.editor.container.$).find(".cke_wysiwyg_div");
 if($frame) $frame.attr("title", "");
});


    })
});