define(['jquery',  'bootstrap', ], function ($) {
    $(document).ready(function () {
 
        console.log(" ajax-quizz-teacher chargé "); 

        

        setTimeout("location.reload(true);", 2000);



            // // -----------------------------------------------------
            // // Ces 4 lignes permettent d'ouvrir la connexion
            // // -----------------------------------------------------

            // var loc = window.location ;
            // var wsStart = 'ws://' ;
            // if (loc.protocol == 'https:') { wsStart = 'wss://' }
            // var endpoint = wsStart + loc.host + "/ws/tool/" ;
            // // -----------------------------------------------------
            // // -----------------------------------------------------
            // // -----------------------------------------------------

            // // -----------------------------------------------------
            // // Ouverture de la Soket
            // // -----------------------------------------------------
            // var socket = new WebSocket(endpoint) ;
            // console.log(socket);

            // // -----------------------------------------------------
            // // Message reçu du serveur
            // // -----------------------------------------------------
            // socket.onmessage = function(e){
            //         var djangoData = JSON.parse(e.data);
            //         console.log(djangoData) ;
            //         $("#nb_players").text(djangoData.value) ;  
            //     }

            // socket.onopen  = function(e){
            //         console.log("onopen") ;
            //     }
            // socket.onerror = function(e){
            //         console.log("onerror") ;
            //     }
            // socket.onclose = function(e){
            //         console.log("onclose") ;
            //     }







    });
});