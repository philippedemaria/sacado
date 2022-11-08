define(['jquery',  'bootstrap', 'ui' , 'ui_sortable' , 'uploader','config_toggle'], function ($) {
    $(document).ready(function () {


    console.log(" class_image chargé ");

        $("#id_calculator").prop("checked", false);   
        $("#id_is_publish").prop("checked", true); 



        $("#id_imagefile").withDropZone("#drop_zone", {
            action: {
              name: "image",
              params: {
                preview: true,
              }
            },
          });



        $('body').on('change', '#id_imagefile' , function (event) {
            loadfile( '#id_imagefile' ) ;
         });


        function loadfile(id_url) {

            const file = $(id_url)[0].files[0];
            const reader = new FileReader();

            reader.addEventListener("load", function (e) {
                                                var image = e.target.result ;   
                                                $(".this_bg").css("background-image", "url("+image+")" );
                                                $(".this_bg").css("background-repeat", "no-repeat" );
                                            }) ;

            if (file) { 
              reader.readAsDataURL(file);
            }            

          }


 
    });
});