define(['jquery', 'bootstrap' ], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-accounting.js OK");


        $(".details_beneficiaire").hide();

        $("body").on('focus', '#id_beneficiaire', function (event) { 
            $(".details_beneficiaire").show();
        });      

        $("body").on('change', '#id_school', function (event) { 
            $(".details_beneficiaire").hide();
        });


        $(document).on('click', '.add_more', function (event) {


                var total_form = $('#id_details-TOTAL_FORMS') ;
                var totalForms = parseInt(total_form.val())  ;

                var thisClone = $('#rowToClone');
                rowToClone = thisClone.html() ;

                $('#formsetZone').append(rowToClone);

                $('#duplicate').attr("id","duplicate"+totalForms) 
                $('#cloningZone').attr("id","cloningZone"+totalForms) 

                $('#duplicate'+totalForms).find('.delete_button').html('<a href="javascript:void(0)" class="btn btn-danger remove_more" ><i class="fa fa-trash"></i></a>'); 
                $('#duplicate'+totalForms).find("input[type='checkbox']").bootstrapToggle();

                $("#duplicate"+totalForms+" input").each(function(){ 
                    $(this).attr('id',$(this).attr('id').replace('__prefix__',totalForms));
                    $(this).attr('name',$(this).attr('name').replace('__prefix__',totalForms));
                });

                console.log(totalForms+1);
                total_form.val(totalForms+1);
            });



        $(document).on('click', '.remove_more', function () {
            var total_form = $('#id_details-TOTAL_FORMS') ;
            var totalForms = parseInt(total_form.val())-1  ;

            $('#duplicate'+totalForms).remove();
            total_form.val(totalForms)
        });


        $(".abonnement_div").hide();


        $("body").on('change', '#id_is_abonnement', function (event) {

                var value = $("#id_school").val() ;

                        if (  value == ""  )
                        {
                            alert("Vous ne pouvez pas créer d'abonnement sans renseigner un établissement déjà créé.");
                            $("#id_school").focus();                    
                            $('#id_is_abonnement').prop('checked', false);
                        }
                        else 
                        {
                            $(".abonnement_div").toggle();  
                        }



                }); 



        $("body").on('change', '#id_mode', function (event) {  

            var id_mode = $("#id_mode").val() ;

            if(id_mode == "Période de test")

                {

                    alert("Renseigner la date de fin de la période d'essai");
                    $("#id_date_stop").val("");
                    $("#id_date_stop").focus();
                }

        });

        // $("body").on('change', '#id_mode', function (event) {  

        //     var id_mode = $("#id_mode").val() ;

        //     if(id_mode == "Période de test")

        //         {

        //         var date_start = $("#id_date_start").val(); 

        //         var date_tab = date_start.split(" ");

        //         if (date_tab[0].indexOf("/") >= 0)
        //             { 
        //                 var date_split = date_tab[0].split("/"); 
        //                 var day   = date_split[0] ;
        //                 var month = date_split[1] ;
        //                 var year  = date_split[2] ;
        //             }
        //         else
        //             { 
        //                 var date_split = date_tab[0].split("-"); 
        //                 var day   = date_split[2] ;
        //                 var month = date_split[1] ;
        //                 var year  = date_split[0] ;
        //             }

        //         var date_stop = year +"-"+ month +"-"+ day +" 00:00"

        //         $("#id_date_stop").val(date_stop);
        //         }

        // });

    });

});
 

 
 

 
 
 