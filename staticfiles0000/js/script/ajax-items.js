define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-items.js OK --");

        if ( $('#id_model').val() == "3") { $('#show_skw').hide(500) ;} else { $('#show_skw').show() ; }     

        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('#id_model').on('change', function (event) {
            let id_model = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            if ( id_model == "3") { $('#show_skw').hide(500) ;} else { $('#show_skw').show() ; }

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'id_model': id_model,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax/create_answer",
                    success: function (data) {
                    $("#model_items").html("").append(data.html); 
                    }
                }
            )
        });








        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.show_item').on('click', function (event) {
            let item_id = $(this).attr("data-item_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'item_id': item_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax/show_this_item",
                    success: function (data) {
                    $("#modal_title").html("").append(data.title) 
                    $("#show_after_ajax").html("").append(data.html)  
                    }
                }
            )
        });



    });
});