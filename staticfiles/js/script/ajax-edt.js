define(['jquery', 'bootstrap'], function ($) {
    $(document).ready(function () {
        console.log("chargement JS ajax-adhesion.js OK");


 
        $('.get_this_group_to_this_slot').on('change', function (event) {
            
                        fill_the_edt($(this),false,false)
        }); 
 

         $('.get_this_group_to_this_slot_half_time_A').on('change', function (event) {
        
            fill_the_edt($(this),true,true)

        }); 

         $('.get_this_group_to_this_slot_half_time_B').on('change', function (event) {
        
            fill_the_edt($(this),true,false)

        }); 

        function fill_the_edt($this,half,even){

            let id_group = $this.val();
            let slot     = $("#this_slot").val();
            let csrf_token = $("input[name='csrfmiddlewaretoken']").val();

            $.ajax(
                {
                    type: "POST",
                    dataType: "json",
                    data: {
                        'id_group': id_group,
                        'slot'    : slot,
                        csrfmiddlewaretoken: csrf_token
                    },
                    url: "my_edt_group_attribution",
                    success: function (data) {

                        if ( parseInt(id_group) != 0){ 
                            $('#slot-'+slot).attr('style',data.style);
                            time = data.name ;
                            hf_slot = 0 ;
                            hf_even = 0 ;
                            if (half) 
                                { 

                                if (even) 
                                    { 
                                        time = '1sem/2 A : '+data.name  ; hf_even = 1; 
                                    }
                                else{
                                    time = '1sem/2 B: '+data.name ; hf_even = 0; 
                                    }
                                    hf_slot = 1; 
                                }

                            $('#slot-'+slot).html(time);
                            $('#edt_modal').modal('toggle');
                            $('#annual_slot-'+slot).val(data.group_id+'-'+slot+'-'+hf_slot+'-'+hf_even);                            
                        }
                        else{
                            $('#slot-'+slot).attr('style',data.style);
                            $('#slot-'+slot).html(data.name);
                            $('#edt_modal').modal('toggle');
                            $('#annual_slot-'+slot).val("");  
                        }
                    }
                }
            )
        }




        $('.get_this_slot').on('click', function (event) { 

            let data_slot = $(this).data("slot");
            $("#this_slot").val(data_slot) ;

        });  

 

 


    });

});

