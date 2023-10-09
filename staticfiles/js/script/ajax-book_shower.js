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



 
        $(document).on('click', '.display_correction_bloc_button' , function (event) {
            
            let source_id = $(this).data("source_id");
            let type_id   = $(this).data("type_id");
 
            if ($(this).children().first().hasClass('text-success')){ var status = "on";}
            else { var status = "off";}

 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'type_id'   : type_id,
                        'source_id' : source_id ,
                        'status'    : status ,
                    },
                    url: "../../ajax_display_correcion_bloc",
                    success: function (data) {
 
                        if(type_id == "0") { 
                            $("#cc_chapter"+source_id).addClass(data.css);
                            $("#cc_chapter"+source_id).removeClass(data.nocss);
                        }
                        else if (type_id == "1") { 
                            $("#cc_page"+source_id).addClass(data.css);
                            $("#cc_page"+source_id).removeClass(data.nocss);
                        }
                        else if(type_id == "2") { 
                            $("#cc_paragraph"+source_id).addClass(data.css);
                            $("#cc_paragraph"+source_id).removeClass(data.nocss);

                            $(".these_blocs").addClass(data.css);
                            $(".these_blocs").removeClass(data.nocss);


                        }
                        else if(type_id == "3") { 
                            $("#cc_bloc"+source_id).addClass(data.css);
                            $("#cc_bloc"+source_id).removeClass(data.nocss);
                        }

                    }
                }
            )
        }); 




           
        $(document).on('click', ".show_this_bloc_correction" , function (event) {

            var this_html = $(this).data("correction") ; 
            $("#book_shower_page").modal('toggle');
            $("#book_shower_correction_content").html(this_html);

        }); 

    
        $(document).on('change', "#customRanger" , function (event) {

            var value = $(this).val() ; 

            $("#book_shower_correction_content").css("font-size",value*12);

            $("#book_shower_correction_content img").css("width",value*60+'%');           

        });  
 



});

});

 