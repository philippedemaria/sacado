define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {

        console.log("chargement JS update_school_admin.js OK");




        $(document).on('click', '.paiement' , function (event) {
            $("#aid").val( $(this).data('aid')) ;

        });
  


        $(document).on('change', '#id_date_stop' , function (event) {
             
            var d = new Date();
            var from = $(this).val().split("-");
            var f = new Date(from[0], from[1]-1 , from[2]);

            if(f > d) {
                $("#date_receipt").removeClass("no_visu_on_load");
            } 
            else{
                $("#date_receipt").addClass("no_visu_on_load");
            }


        });





    });
});

 
