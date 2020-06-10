define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
 
   
  // Publier un cours via le menu droit
        $('.students_handler').on('click', function (event) {
            let student_id = $(this).attr("data-student_id");
            let content_id = $(this).attr("data-content_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'student_id': student_id,
                        'content_id': content_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../../../../ajax/homework_render/",
                    success: function (data) {
                          $("#student_homework_render").html("").append(data.html) 
              
                    }
                }
            );
        });  
      
 


 
 
 
        console.log("chargement JS ajax-homework.js OK ======== ");

    });
});  