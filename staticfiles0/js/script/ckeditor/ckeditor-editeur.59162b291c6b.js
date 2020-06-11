define(['jquery', 'ckeditor', 'ckeditor_jquery'], function ($) {
    $(document).ready(function () {
        var editeur = CKEDITOR.instances.editeur;
        if (editeur) {
            editeur.destroy(true);
        }
        CKEDITOR.replace('editeur', {
            filebrowserBrowseUrl: './plugins/ckfinder/ckfinder.html',
            filebrowserImageBrowseUrl: './plugins/ckfinder/ckfinder.html?type=Images',
            filebrowserUploadUrl: './plugins/ckfinder/core/connector/php/connector.php?command=QuickUpload&type=Files',
            filebrowserImageUploadUrl: './plugins/ckfinder/core/connector/php/connector.php?command=QuickUpload&type=Images'
        });


CKEDITOR.on("instanceReady", function(e) {
 var $frame = $(e.editor.container.$).find(".cke_wysiwyg_div");
 if($frame) $frame.attr("title", "");
});
 
  var c = document.body.children;
 
  for (i = 0; i < c.length; i++) {

    c[i].removeAttribute("title");
    }


    })
});