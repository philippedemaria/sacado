define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
 

    
 
        console.log("---- NEW test ajax-new-customer.js ---") ;  

        $('#rne').on('blur', function (event) {

            let rne = $(this).val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'rne'   : rne,           
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "ajax_new_customer",
                    success: function (data) {

                       $('#id_school').html("").html(data.html)     ;
                        
                    }
                }
            )
        });


        
  


});

});
