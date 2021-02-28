define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-exercise-canvas.js OK");

 

  ///////////////////////////////////////////////////////
        $("#text_zone_div").hide();
        $("#canvas_zone_div").hide();

        $("#text_zone").on('click', function (){ 
            $("#text_zone_div").show(300);
            $("#canvas_zone_div").hide(300);
            $(this).removeClass("btn-default").addClass("btn-primary");
            $("#canvas_zone").addClass("btn-default").removeClass("btn-primary");
        })

        $("#canvas_zone").on('click', function (){ 
            $("#text_zone_div").hide(300);
            $("#canvas_zone_div").show(300);
            $(this).removeClass("btn-default").addClass("btn-primary");
            $("#text_zone").addClass("btn-default").removeClass("btn-primary");
        })

        ///////////////////////////////////////////////////////
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


        $("#myCanvas").on("mouseover", function(){    
            paint('true') ;
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
                        var init_y = event.clientY - 171 ; 

                        console.log(init_x,init_y);

                        ctx.lineTo(init_x,init_y);
         
                        if (flag =="false"){
                            ctx.strokeStyle = "white" ;
                        }
                        ctx.stroke();

                    })


                    $("#myCanvas").mouseup(function(event){
                        
                        $("#myCanvas").unbind("mousemove");
                        flag = "true" ;
                        ctx.closePath();
                    })

            })
        }


        var interval = setInterval( save_canvas, 5000)




        function save_canvas(){

            let customexercise_id = $("#customexercise_id").val();
            let parcours_id       = $("#parcours_id").val();
            let csrf_token        = $("input[name='csrfmiddlewaretoken']").val();
            
            console.log('start !');
 
            var image = document.getElementById("myCanvas").toDataURL("image/png");
            image = image.replace('data:image/png;base64,', '');
            $.ajax({
                type: 'POST',
                url: "../../ajax_save_canvas",
                data: { "image" : image ,
                        'customexercise_id': customexercise_id,
                        'parcours_id': parcours_id,
                        csrfmiddlewaretoken: csrf_token
                    },
                dataType: 'json',
                success: function(data) {

                    if (data.image){
                    image = loadImage(data.image);
                    ctx.drawImage(image, canvas.width , canvas.height , 0, 0)
                    console.log("image loaded")                        
                    }

 
                    console.log('Image saved successfully !');
                }
            });
 
 
        }
      




});

});

