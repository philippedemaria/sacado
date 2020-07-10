define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-group-many.js OK");




        var total_form = $('#id_form-TOTAL_FORMS') ;
        var totalForms = parseInt(total_form.val())  ;
        var FormToDuplicate = totalForms - 1 ;
          
    $('.add_more').on('click', function (event) {

console.log(totalForms); 
 
        var tr_object = $('#duplicate').clone();
        tr_object.attr("id","duplicate"+totalForms) 
        tr_object.attr("style","display:block") 
 

        tr_object.appendTo("#formsetZone");

 
        $(tr_object).find('.delete_button').html('<a href="javascript:void(0)" class="btn btn-danger remove_more" >Supprimer</a>'); 

        total_form.val(totalForms+1)

    });

        $(document).on('click', '.remove_more', function () {
 
            $('#duplicate'+totalForms).remove();
            total_form.val(FormToDuplicate)
        });
                
    });

});
 

 
 

 
 
 