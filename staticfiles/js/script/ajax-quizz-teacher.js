define(['jquery',  'bootstrap', ], function ($) {
    $(document).ready(function () {
 
 
            console.log(" ajax-quizz-teacher chargé ");


            var loc = window.location ;
            var wsStart = 'ws://' ;

            if (loc.protocol == 'https:') { wsStart = 'wss://' }

            var endpoint = wsStart + loc.host + "/ws/tool/" ;


            var socket = new WebSocket(endpoint) ;
            socket.onmessage = function(e){
                
                    var djangoData = JSON.parse(e.data);
                    console.log(djangoData) ;

                    $("#nb_players").text(djangoData.value) ;  


                }





    });
});