define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
 
 
        console.log("---- ajax-list-group.js ---") ;  


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

 
