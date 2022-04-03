define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-adhesion.js OK");



 
        $('.adh_select').on('click', function (event) {
            
            let data_id = $(this).attr("data_id");
            $("#adh_id").val(data_id);
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'data_id': data_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_remboursement",
                    success: function (data) {
                        console.log(data.remb) ;
                        $('#remb').html("").html(data.remb);
                        $('#jour').html("").html(data.jour);
                    }
                }
            )
        }); 


        $('.validate_renewal').attr("disabled",true); 
        var liste = [] ;
 
        $('.renewal_user_class').on('click', function (event) {

            let data_name = $(this).attr("data_name");
            let data_id = $(this).val()
            let level = $("#level"+data_id).val();
            levels = ["Cours Préparatoire", "Cours Elémentaire 1", "Cours Elémentaire 2","Cours Moyen 1","Cours Moyen 2","Sixième", "Cinquième", "Quatrième","Troisième","Seconde","Première","Terminale"]

            if (!$(this).is(':checked'))
            {
            desconstruct_user("Enfant",data_id) ; 
            }
            else
            {
            construct_user("Enfant",data_name, levels[level-1] ,data_id ) ; 
         
            }


        });    



        function construct_user(statut,name,level,id){
                let nb_child = $("#nb_child").val();
                nb =  parseInt(nb_child);

                var div = "<div class='renewal_user selector' id="+id+"><label>"+statut+"</label><div>"+ name +"<br/> "+ level +"</div></div>" ;  
                $("#show_confirm_renewal").append(div) ;

                 liste.push(id); 
                $('#renewal'+id).parent().parent().addClass("selector") ;

 
                if (nb ==  parseInt(liste.length)) {  
                    $('.renewal_user').hide();
                    $('.selector').show();
                    }
                $('.validate_renewal').attr("disabled",false); 
            }

        function desconstruct_user(statut,id){
                let nb_child = $("#nb_child").val();

                $("#"+id).remove();  
                $('#renewal'+id).parent().parent().removeClass("selector") ;
                $('.renewal_user').show();
                liste.splice(liste.indexOf(id),1);  
            }



            $("#id_username").on('change', function () {
 
                let username = $("#id_username").val();
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
     
                $.ajax({
                    url: '/account/ajax/userinfo/',
                    type: "POST",
                    data: {
                        'username': username,
                        csrfmiddlewaretoken: csrf_token,    
                    },
                    dataType: 'json',
                    success: function (data) {
                        $("#ajaxresult"+i).html(data["html"]);

                         $("#div_username").show();
                         $("#verif_username").html( $("#id_username").val() );

                         $("#id_save").show();


                    } 
                }); 

            });

 

     



            $("#id_last_name").on('change', function () {
                    $("#div_display").show() 
                 $("#div_last_name").show();
                 $("#verif_last_name").html( $("#id_last_name").val() );

            });


            $("#id_first_name").on('change', function () {
                    $("#div_display").show() 
                 $("#div_first_name").show();
                 $("#verif_first_name").html( $("#id_first_name").val() );

            });
 


            $("#id_level").on('change', function () {
                    $("#div_display").show() 
                 $("#div_level").show();
                 $("#verif_level").html( $('option[value="'+$("#id_level").val()+'"]')   );

            });


            $("#id_email").on('change', function () {
                    $("#div_display").show() 
                 $("#div_email").show();
                 $("#verif_email").html( $("#id_email").val() );

            });
 




    });

});

