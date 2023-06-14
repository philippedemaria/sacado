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
                        $('#select_users').show()    ;


                        users = data["users"] ; 

                        $('select[name=this_user_id]').empty("");

                        if (users.length >0)
                        { for (let i = 0; i < users.length; i++) {
                                    
                                    let users_id   = users[i][0];
                                    let users_name =  users[i][1]  ;
                                    let option     = $("<option>", {
                                        'value': Number(users_id),
                                        'html': users_name
                                    });
                                    $('select[name=this_user_id]').append(option);
                                }
                        }
                        else
                        {
                                    let option = $("<option>", {
                                        'value': 0,
                                        'html': "Aucun contenu disponible"
                                    });
                            $('select[name=this_user_id]').append(option);
                        }



                        
                    }
                }
            )
        });


        
  


});

});
