define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-book.js OK");

    
           
        $(document).on('click', ".to_projection" , function (event) {

            var this_html = $(this).html() ; 

            $("#book_shower_page_content").html(this_html);

        }); 



           
        $(document).on('change', "#customRange" , function (event) {

            var value = $(this).val() ; 


            $("#book_shower_page_content").css("font-size",value*12);
            $("#book_shower_page_content").css("line-height",'1.3em');
            $("#book_shower_page_content table tr td").css("font-size",value*12);
            $("#book_shower_page_content img").css("width",'200%'); 
            $("#book_shower_page_content img").css("height",'200%'); 
        }); 



 
        $(document).on('click', '.display_correction_bloc_button' , function (event) {
            
            let source_id = $(this).data("source_id");
            let type_id   = $(this).data("type_id");
            let paragraph_id   = $(this).data("paragraph_id");
            let is_correction   = $(this).data("is_correction");
            if ($(this).children().first().hasClass('text-success')){ var status = "on";}
            else { var status = "off";}

            $("#spinner-"+type_id+"-"+source_id).html("<i class='fa fa-spinner fa-spin'></i>")
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'type_id'   : type_id,
                        'source_id' : source_id ,
                        'is_correction' : is_correction ,
                        'status'    : status ,
                    },
                    url: "../../ajax_display_correction_bloc",
                    success: function (data) {
 
                        if(type_id == "0") { 


                            if(is_correction){
                                $("#cc_chapter_cor"+source_id).addClass(data.css);
                                $("#cc_chapter_cor"+source_id).removeClass(data.nocss);
    
                                $(".all_these_blocs_cor").addClass(data.css);
                                $(".all_these_blocs_cor").removeClass(data.nocss);
                            }
                            else{
                                $("#cc_chapter"+source_id).addClass(data.css);
                                $("#cc_chapter"+source_id).removeClass(data.nocss);
    
                                $(".all_these_blocs").addClass(data.css);
                                $(".all_these_blocs").removeClass(data.nocss);
                            }



                        }
                        else if (type_id == "1") { 

                            if(is_correction){
                                $("#cc_page_cor"+source_id).addClass(data.css);
                                $("#cc_page_cor"+source_id).removeClass(data.nocss);

                                $(".all_these_blocs_cor").addClass(data.css);
                                $(".all_these_blocs_cor").removeClass(data.nocss);
                            }
                            else{
                                $("#cc_page"+source_id).addClass(data.css);
                                $("#cc_page"+source_id).removeClass(data.nocss);
    
                                $(".all_these_blocs").addClass(data.css);
                                $(".all_these_blocs").removeClass(data.nocss);
                            }

                        }
                        else if(type_id == "2") { 

                            if(is_correction){
                                $("#cc_paragraph_cor"+source_id).addClass(data.css);
                                $("#cc_paragraph_cor"+source_id).removeClass(data.nocss);
    
                                $(".these_blocs_cor"+paragraph_id).addClass(data.css);
                                $(".these_blocs_cor"+paragraph_id).removeClass(data.nocss);
                            }
                            else{
                                $("#cc_paragraph"+source_id).addClass(data.css);
                                $("#cc_paragraph"+source_id).removeClass(data.nocss);
    
                                $(".these_blocs"+paragraph_id).addClass(data.css);
                                $(".these_blocs"+paragraph_id).removeClass(data.nocss);
                            }

                        }
                        else if(type_id == "3") { 
                            if(is_correction){
                                $("#cc_bloc_cor"+source_id).addClass(data.css);
                                $("#cc_bloc_cor"+source_id).removeClass(data.nocss);  
                            }
                            else{
                                $("#cc_bloc"+source_id).addClass(data.css);
                                $("#cc_bloc"+source_id).removeClass(data.nocss);
                            }
                        }
                        $("#spinner-"+type_id+"-"+source_id).html("")
                    }
                }
            )
        }); 

 

           
        $(document).on('click', ".show_this_bloc_correction" , function (event) {

            const bloc_id = $(this).data("bloc_id") ; 

            
            const this_title_bloc = $("#title_bloc"+bloc_id+" .bloc_title").html(); 

            const this_content_html = $("#book_shower_this_correction"+bloc_id).html(); 

            const this_html = this_title_bloc+this_content_html;


            $("#book_shower_correction_content").html(this_html);

        }); 

    
        $(document).on('change', "#customRanger" , function (event) {

            var value = $(this).val() ; 

            $("#book_shower_page_content").css("font-size",value*12);
            $("#book_shower_page_content").css("line-height",'1.3em');
            $("#book_shower_page_content img").css("width",'200%'); 
            $("#book_shower_page_content img").css("height",'200%'); 
        });  
 


 

});

});

 