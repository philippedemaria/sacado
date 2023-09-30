define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-organiser.js OK");
 
 

 

            $(document).on('click', '#duplication_document', function (event) {
                    var  document_id = $(this).data("document_id");  
                    var  document_title = $(this).data("document_title");  

                    $("#this_document_id").val(document_id) ;
                    $("#this_document_title").html(document_title) ;
                    $("#this_document_label").html(document_title) ;
                });
            
            $(document).on('click', "#duplicate_button_action" , function () {

                    event.preventDefault();   
                    my_form = document.querySelector("#duplicate_form");
                    var form_data = new FormData(my_form); 
         
                    let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
         
                    $.ajax(
                        {
                            type: "POST",
                            dataType: "json",
                            traditional : true,
                            data: form_data,
                            url: "../../../../bibliotex/exercise_bibliotex_duplicate",
                            success: function (data) {
                                alert(data.validation);

                            },
                                cache: false,
                                contentType: false,
                                processData: false
                        }
                    )
                });









});

});

 