define(['jquery', 'bootstrap','mathjax'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS list_knowledge_by_level.js OK");




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



        MathJax.Hub.Queue(["Typeset",MathJax.Hub]);

    });

});

