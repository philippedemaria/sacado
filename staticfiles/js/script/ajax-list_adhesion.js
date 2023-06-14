define(['jquery', 'bootstrap' ], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-list_accounting.js OK");

 

 
        $('#month').on('change', function (event) {
            let month = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
 
                        'month': month,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_total_month",
                    success: function (data) {
                       $(".this_tr_all").removeClass("selected_account");
                       $("#this_month").html(data.html) ;

                       if (data.len > 0){

                            for (var i = 0; i < data.len ; i++) {
                                $("#this_tr_"+data.rows[i]).addClass("selected_account");
                            }

                       }

                    }
                }
            )
        });





 
        $('.period').on('change', function (event) {

            let from_date = $("#from_date").val();
            let to_date   = $("#to_date").val();


            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
 
                        'from_date': from_date,
                        'to_date'  : to_date,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_total_period",
                    success: function (data) {

                       $("#this_period").html(data.html) ;
                       $(".this_tr_all").removeClass("selected_account");

                       if (data.len > 0){

                            for (var i = 0; i < data.len ; i++) {
                                $("#this_tr_"+data.rows[i]).addClass("selected_account");
                            }

                       }

                    }
                }
            )
        });





 
        $('.displayer_button').on('click', function (event) {

            let customer_id = $(this).data('customer_id');
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
 
                        'customer_id': customer_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_display_button",
                    success: function (data) {

                       $("#display_button"+customer_id).html(data.html) ;

                    }
                }
            )
        });


 
        $('#display_button').on('click', function (event) {

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            if (confirm("Confirmer l'affichage de TOUS les boutons d'adhésion ?")) {

                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: "ajax_display_all_buttons",
                        success: function (data) {

                           $(".displayer_button").html(data.html) ;

                        }
                    }
                )
                } 

        });







    });

});
 

 
 

 
 
 