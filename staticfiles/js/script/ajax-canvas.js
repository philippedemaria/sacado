define(['jquery', 'bootstrap' ], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-canvas-painter.js OK");


 




        var canvas      = document.getElementById("myCanvas");
        var ctx         = canvas.getContext('2d');
        canvas.width    = 700;
        canvas.height   = 500;



        // Couleur
        $("#colorpicker").on("change", function(){    
            ctx.strokeStyle = $(this).val() ;
        });
        // Epaisseur de trait
        $("#thickness").on("change", function(){    
            ctx.lineWidth = $(this).val() ;
        });

        // Ecriture tapuscrite
        $("#text").on("click", function(){
            ctx.font = "14px Arial"   ;
            ctx.strokeStyle = $("#colorpicker").val() ;
            msg ="hello";
            w=400;
            h=200;
            ctx.fillText(msg,w,h); console.log(msg) ; 


            $(".btn").addClass("btn-default").removeClass("btn-primary");
            $(this).addClass("btn-primary");

        });


        // pencil
        $("#pencil").on("click", function(){ 

            $(".btn").addClass("btn-default").removeClass("btn-primary");
            $(this).addClass("btn-primary");
            $("#myCanvas").on("mouseover", function(){    
                paint('true') ;
            });
        });



        // Effacer tout le canvas
        $("#clear").on("click", function(){    
            ctx.fillStyle = "white";
            ctx.fillRect(0,0,canvas.width,canvas.height);
        });


        // Effacer une partie
        $("#erasor").on("click", function(){    
            paint('false') ;
        });


        function paint(flag){
            $("#myCanvas").mousedown(function(event){ 
                    ctx.beginPath();


                    $("#myCanvas").mousemove(function(event){
                        
                        var init_x = event.clientX - 136;
                        var init_y = event.clientY - 98 ; 

                        console.log(init_x,init_y);

                        ctx.lineTo(init_x,init_y);
         
                        if (flag =="false"){
                            ctx.strokeStyle = "white" ;
                        }
                        ctx.stroke();

                    })


                    $("#myCanvas").mousedown(function(event){
                        
                        $("#myCanvas").unbind("mousemove");
                        flag = "true" ;
                        ctx.closePath();
                    })

            })
        }



        // // Prévisualisation d'mage
        // $("#getImage").on("change", function(){    
        //     previewImage($("#getImage").val()) ;
        // });



        // function previewImage(input){ console.log("ici") ; 
        //     var reader = new FileReader();
        //     reader.onload = function (e){
        //         document.getElementById("preview");
        //     };
        //     reader.readAsDataURL(input.files[0]);
        // }



        $("#saver").on("click", function(){    
   
            var canvas = document.getElementById("myCanvas");
            var data = canvas.toDataURL("image/jpeg");
            let customexercise_id = $("#customexercise_id").val() ;

            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();
 
            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'customexercise_id': customexercise_id,
                        'student_id': student_id,
                        'data_canvas' : data,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "ajax_save_canvas",
                    success: function (data) {
                        console.log("success");
                    }
                }
            )






        });










    }); 

});