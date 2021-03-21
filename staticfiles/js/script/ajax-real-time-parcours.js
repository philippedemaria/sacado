define(['jquery',  'bootstrap', ], function ($) {
    $(document).ready(function () {
 
        console.log(" ajax-real-time-parcours chargé "); 
 


        setInterval(  check_live  , 5000);
 
 
        function check_live(){


                let parcours_id = $("#parcours_id").val();
                let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

                $.ajax(
                    {
                        type: "POST",
                        dataType: "json",
                        data: {
                            'parcours_id': parcours_id,
                            csrfmiddlewaretoken: csrf_token
                        },
                        url: "../ajax_real_time_live",
                        success: function (data) {

                            line = data.line.split("=====") ;
                            cell = data.cell.split("=====") ;
                            result = data.result.split("=====") ;

                            line.forEach(line_split);
                            cell.forEach(cell_split);

                            function line_split(item) {
                                $("#"+item).addClass("live").removeClass("no_live") ;
                            }

                            function line_split(item) {
                                $("#"+item).addClass("live").removeClass("no_live") ;
                            }


                            function cell_split(item,index) {
                                $("#"+item).html( result[index])  ;

                                console.log("#"+item,  result[index]);



                            }




 





                        }
                    }
                )
            }         


 

 


    });
});