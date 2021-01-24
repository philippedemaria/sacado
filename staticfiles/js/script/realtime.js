define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
    	{
    		console.log("---- realtime.js ---") ;	


 



            var loc = window.location ;
            var wsStart = 'ws://' ;

            if (loc.protocol == 'https:') { wsStart = 'wss://' }

            var endpoint = wsStart + loc.host + "/ws/realtime/" ;

            console.log(endpoint);

            var socket = new WebSocket(endpoint) ;

            socket.onmessage = function(e){
                
                var djangoData = JSON.parse(e.data);
                console.log(djangoData) ;

                $("#app").text(djangoData.value) ;  












            }	

        };
  
    });

});
 