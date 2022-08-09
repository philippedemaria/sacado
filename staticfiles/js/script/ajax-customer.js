define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
 

    
 
        console.log("---- NEW test ajax-customer.js ---") ;  

        $('.status_id').on('change', function (event) {

            let status_id = $(this).val();
            let customer_id = $("#customer_id").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    traditional: true,
                    data: {
                        'status_id'   : status_id,
                        'customer_id' : customer_id,             
                        csrfmiddlewaretoken: csrf_token
                    },
                    url : "ajax_customer/",
                    success: function (data) {

 
                        
                    }
                }
            )
        });


        
  


});

});
