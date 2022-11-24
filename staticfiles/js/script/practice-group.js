define(['jquery','bootstrap','ui'], function ($) {
    $(document).ready(function () {

        console.log("chargement JS practice-group.js OK");


 
        // Affiche dans la modal le modèle pour récupérer un exercice custom
        $('body').on('click', '.show_kgroup' , function (event) {

            let stamp = $(this).data('stamp');
            $('.groups').addClass('no_visu_on_load');
            $('#kgroup'+stamp).removeClass('no_visu_on_load');
            $('.initial_group').addClass('no_visu_on_load');
            $('.show_kgroup').removeClass('btn btn-sacado');
            $('#show_kgroup'+stamp).addClass('btn btn-sacado');

            
         });



          $( function() {
            $( ".draggable" ).draggable(
                {
                    appendTo : '.droppable', 
                    revert : true,
                }
                );
            $( ".droppable" ).droppable({
                    drop: function( event, ui ) {
                        $(this).append( $(ui.draggable[0])  );

                        var nb_group       = parseInt($(this).data('group'))-1;
                        var student_id     = $(ui.draggable[0]).data('student') ;
                        var student_id_str = student_id.toString();
                        var old_str        = $('#printable').val();


                        var old_list = old_str.split("####") ;

 
                        var new_list = [];
                        var new_str  = "";

                        for (i=0;i<old_list.length;i++){

                            old_sublist = old_list[i].split('##');

                            idx = $.inArray(student_id_str, old_sublist)
                            if( idx > -1 ){ 
                                old_sublist.splice(idx, 1);
                            }
                            new_sub_str = old_sublist.join("##");

                            if (i == nb_group){
                                new_sub_str = new_sub_str+"##"+student_id_str ;
                            }
                            if (new_sub_str.length)
                                {new_list.push(new_sub_str)} ;
                        }

                        new_list_print = new_list.join("####");
                        $('#printable').val(new_list_print);


                        $('#is_homogene').val(new_list_print);
                        $('#these_knowledges').val(new_list_print);

                    }
                });
          });
    });
});