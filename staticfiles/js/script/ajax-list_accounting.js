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














    });

});
 

 
 

 
 
 