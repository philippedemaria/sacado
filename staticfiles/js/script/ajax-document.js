define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-document.js OK");



        // Affiche dans la modal le modèle pour récupérer un exercice custom
        $('.document_viewer').on('click', function (event) {

            let document_id = $(this).attr("data-document_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'document_id': document_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_shower_document",
                    success: function (data) {          

 
                        $('#this_document_body').html(data.html);
                    }
                }
            )
         });







 





    });

});

