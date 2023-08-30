define(['jquery', 'bootstrap', 'ui', 'ui_sortable'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-list-question-flash.js OK --");



        $('body').on('click', '.qf_publisher' , function (event) {  

            var qflash_id  = $(this).data("qflash_id");

            if ($('#qf_publish'+qflash_id).hasClass("btn-danger")) { var is_publish = "0";}
            else { var is_publish = "1";}

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",                    
                    traditional: true, // Permet d'envoyer une liste.
                    data: {
                        'is_publish' : is_publish,
                        'qflash_id'  : qflash_id,
                    },
                    url: "ajax_publish_question_flash",
                    success: function (data) {

                        $('#qf_publish'+qflash_id).html("").html(data.html);
                        

                        if ($('#qf_publish'+qflash_id).hasClass("btn-danger")) {
                            $('#qf_publish'+qflash_id).removeClass("btn-danger");
                            $('#qf_publish'+qflash_id).addClass("btn-success");
                        }
                        else{
                            $('#qf_publish'+qflash_id).removeClass("btn-success");
                            $('#qf_publish'+qflash_id).addClass("btn-danger");
                        }
                    }
                }
            )
         });



    });
});