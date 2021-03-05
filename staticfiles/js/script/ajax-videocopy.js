define(['jquery',  'bootstrap',  'uploader' ,  ], function ($) {
    $(document).ready(function () {


    console.log(" ajax-video chargé ");

  
        // $('body').on('change', '#id_image' , function (event) {   
        //     previewFile() ;
        //  });      


 
        // function previewFile() {


        //     const file = $('#id_image')[0].files[0];
        //     const reader = new FileReader();

        //     $("#preview").val("") ;  


        //     reader.addEventListener("load", function (e) {
        //                                         var image = e.target.result ; 
        //                                         $("#preview").attr("src", image );
        //                                     }) ;

        //     if (file) { console.log(file) ;
        //       reader.readAsDataURL(file);
        //     }            

        //   }
 

  
        $('body').on('click', '.this_photo' , function (event) {   

            src = $(this).attr("data-img") ;
            console.log(src) ; 
            $("#this_photo").attr("src",src) ;

         });   










 
    });
});