
define(['jquery', 'ckeditor'], function ($) {
    CKEDITOR.replace('editeur', {
        filebrowserBrowseUrl: './pdw_file_browser/index.php?editor=ckeditor',
        filebrowserImageBrowseUrl: './pdw_file_browser/index.php?editor=ckeditor&filter=image',
        filebrowserFlashBrowseUrl: './pdw_file_browser/index.php?editor=ckeditor&filter=flash'
    });
});

