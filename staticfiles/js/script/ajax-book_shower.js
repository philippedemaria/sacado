define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-book.js OK");

    
           
        $(document).on('click', ".to_projection" , function (event) {

            var this_html = $(this).html() ; 

            $("#book_shower_page_content").html(this_html);

        }); 



           
        $(document).on('change', "#customRange" , function (event) {

            var value = $(this).val() ; 


            $("#book_shower_page_content .bloc_title").css("font-size",value*12);
            $("#book_shower_page_content .bloc_content").css("font-size",value*12);

        }); 










});

});

 