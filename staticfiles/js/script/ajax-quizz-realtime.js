define(['jquery',  'bootstrap' ], function ($) {
    $(document).ready(function () {
 
 
    console.log(" ajax-quizz-realtime chargé ");
 
 
        // Affiche dans la modal la liste des élèves du groupe sélectionné
        $('.this_button_login').on('click', function (event) {

            var student_name = $(this).attr("data-student_name");
            console.log(student_name);
  
         });

 

                document.addEventListener('DOMContentLoaded', function() {
                  const webSocketBridge = new channels.WebSocketBridge();
                  const nl = document.querySelector("#notifylist");
                  
                  webSocketBridge.connect('/tool/');
                  webSocketBridge.listen(function(action, stream) {
                    console.log("RESPONSE:", action);
                    // if(action.event == "New User") {
                    //   var el = document.createElement("li");
                    //   el.innerHTML = `New user <b>${action.username}</b> has joined!`;
                    //   nl.appendChild(el);
                    // }
                  })
                  document.ws = webSocketBridge; /* for debugging */
                })








 
    });
});