define(['jquery',  'bootstrap', ], function ($) {
    $(document).ready(function () {
 
        console.log(" ajax-real-time-parcours chargé "); 
 

        $(".imagefile").on('mouseover', function (event) {
                 $(this).parent().find(".th_real_time_label").addClass("th_real_time_label_hover") ;
                 })

        $(".imagefile").on('mouseout', function (event) {
                 $(this).parent().find(".th_real_time_label").removeClass("th_real_time_label_hover") ;
                 })
            

        check_live();

        //setInterval(  check_live  , 10); 10 millisecondes pour faire sauter le serveur.
 
        function check_live(){


                $(".init").addClass("no_live").removeClass("live")  ; 
                $(".is_tr_display").addClass("allowed_display").removeClass("not_allowed_display")  ;
                $(".init_link").addClass("no_visual_link").removeClass("visual_link")  ;


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
                
                            line.forEach(line_split);
                            cell.forEach(cell_split);


                            function line_split(item) {
                                $("#"+item).addClass("live").removeClass("no_live") ;
                            }


                            function cell_split(item,index) {

                                result = data.result.split("=====") ;                            

                                if (result[index] == "en_compo")   
                                {
                                    $("#"+item).addClass("live").removeClass("no_live")  ; 
                                    $("#"+item).find("span").removeClass("allowed_display").addClass("not_allowed_display")  ;
                                    $("#"+item).find(".init_link").removeClass("no_visual_link").addClass("visual_link")  ;
                                }
                                else
                                {
                                    $("#"+item).html( result[index])  ;                                    
                                }




                            }




 





                        }
                    }
                )
        }         


     
        // var socket = new WebSocket('ws://127.0.0.1:8000/ws/qcm/');

        // socket.onmessage = function(event){
        //     var data = JSON.parse(event.data);
        //     console.log(data);
        //     $('#app').text( data.message ) ;
        // }
 




        //------------------------------------------------------------------------------------------------    
        //------------------------------------------------------------------------------------------------
        //------------------------------------------------------------------------------------------------
        // Gestion du real time
        // Gestion du client qui revçoit un message du webSocket
        //------------------------------------------------------------------------------------------------    
        //------------------------------------------------------------------------------------------------
        //------------------------------------------------------------------------------------------------

        var parcours_id = $("#parcours_id").val();
        var connectionString = 'ws://' + window.location.host + '/qcm/' + parseInt(parcours_id) + '/';

        var socket = new WebSocket(connectionString);

        socket.onmessage = function(event){
            var data = JSON.parse(event.data);
            console.log(data);
            $('#app').text( data.message ) ;
        }
 




















    });
});