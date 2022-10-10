define(['jquery',  'bootstrap' ], function ($) {
    $(document).ready(function () {
 

 	        // Affiche dans la modal le modèle pour récupérer un exercice custom
        $('.get_parcours_from_this_k').on('click', function (event) {

            let k_id = $(this).data("k_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();


            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'k_id': k_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../get_the_k_ia",
                    success: function (data) {
 
 
                    }
                }
            )
         });

       
            // Affiche dans la modal le modèle pour récupérer un exercice custom
        $('.get_parcours_from_this_p').on('click', function (event) {

            let p_id = $(this).data("p_id");
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();


            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'p_id': p_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "../get_the_p_ia",
                    success: function (data) {
 
 
                    }
                }
            )
         });


         
        $('table.display1000').DataTable({
            "pageLength": 1000,
            "ordering": false,
            "retrieve": true,
            "paging": false,
            "info":  false
            });


        $('.input-sm').on('keyup', function (event) {  

        if ($('.input-sm').val() != "")
            { $("tr.opener_e").css("display","table-row")  ; } 
        else 
            { $("tr.opener_e").css("display","none")  ; } 

        });




        $('.opener_k').hide() ;
        $('.opener_e').hide() ;


        $('.opener').on('click' ,function () { 
        $('.opener_k').hide() ;

        if( $(this).hasClass("out") )
        {
            $(".opener ~ .opened"+this.id).show();
            $(this).removeClass("out").addClass("in");
            $(this).find('.fa').removeClass('fa-caret-right').addClass('fa-caret-down'); 
        }
        else 
        {
            $(".opener ~ .opened"+this.id).hide();  
            $(this).removeClass("in").addClass("out");
            $(this).find('.fa').removeClass('fa-caret-down').addClass('fa-caret-right');     
        }

        });



        $('.opener_k').on('click' ,function () { 
        $('.opener_e').hide() ;

        if( $(this).hasClass("out") )
            {
            $(".opener_k ~ .openedk"+this.id).show();
            $(this).removeClass("out").addClass("in");
            $(this).find('.fa').removeClass('fa-caret-right').addClass('fa-caret-down');
            }
        else 
        {
            $(".opener_k ~ .openedk"+this.id).hide();  
            $(this).removeClass("in").addClass("out");
            $(this).find('.fa').removeClass('fa-caret-down').addClass('fa-caret-right');            
        }

        });


 
    });
});