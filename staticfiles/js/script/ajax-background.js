define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-background.js OK");

    


        $(".choicer_background").on('click', function (event) {

            let url = $(this).data("url");
            $("#id_background").val(url);
            $(".choicer_background").addClass("list_avatar_opaque");
            $(this).removeClass("list_avatar_opaque");

        }); 



        
  


});

});

