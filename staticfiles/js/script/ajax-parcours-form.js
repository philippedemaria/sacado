define(['jquery','bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-parcours-complement.js OK");
 

        $("#id_is_publish").on('change', function (event) {
            $('.publication_div').toggle(500);
        });


        $('[type=checkbox]').prop('checked', false);        
        $('#id_is_favorite').prop('checked', true); 


        // Pour le form_parcours
 
         $('#folder_div').hide(); 


         $('#leaf_div').hide(); 



        $(".select_all").click(function(){
            value = $(this).val(); 
            $('#demo'+value+' .selector').not(this).prop('checked', this.checked);
        });


        $(".select_all_sg").click(function(){
            value = $(this).val(); 
            $('#demosg'+value+' .selector').not(this).prop('checked', this.checked);
        });
        
    });
});