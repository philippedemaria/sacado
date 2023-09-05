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
                            var time = data.name ;
                            var hf_slot = 0 ;
                            var hf_even = 0 ;
                            if (half) 
                                { 

                                if (even) 
                                    { 
                                        time = data.name +'[A]' ; hf_even = 1; 
                                    }
                                else{
                                        time = data.name +'[B]'  ; hf_even = 0; 
                                    }
                                    hf_slot = 1; 
                                }

                            
                            $('#edt_modal').modal('toggle');
                            if (  $('#annual_slot-'+slot).val()){
                                var value = $('#annual_slot-'+slot).val() ;
                                var grpi_id = value.split('-')[0];
                                $('#annual_slot-'+slot).val(grpi_id+","+data.group_id+'-'+slot+'-'+hf_slot+'-'+hf_even);  
                                var texte = $('#slot-'+slot).text(); 
                                $('#slot-'+slot).html(texte+","+time);  
                                $('#slot-'+slot).attr('style','background-color:gray;color:white');
                            }
                            else {
                                $('#annual_slot-'+slot).val(data.group_id+'-'+slot+'-'+hf_slot+'-'+hf_even);
                                $('#slot-'+slot).html(time);  
                            }
                                                      
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




        $(document).on('click', '.get_this_slot', function (event) { 

            let data_slot = $(this).data("slot");
            $("#this_slot").val(data_slot) ;

        });  


        $('#edt_listing_text').animate({ scrollTop: $("#this_scrollTop").val() },'slow');

//======================================================================================================
//======================  
//======================================================================================================
        function addDaysToDate(day, intDays) {

            const d = day.split("-") ;
            const y = parseInt(d[0]) ;
            const m = parseInt(d[1]) ;
            const j = parseInt(d[2]) + parseInt(intDays)  ;
            const finalDate = new Date(y,  m , j) 
            const new_day = finalDate.getFullYear()+"-" +finalDate.getMonth()+"-" + finalDate.getDate() ;
            return new_day;
        }


        function str_addDaysToDate(day, intDays) {


            const months = ['Jan.','Fev.','Mars','Avr.','Mai','Juin','Juil.', 'Aout','Sept.','Oct.','Nov.', 'Déc.']

            const d = day.split("-") ;
            const y = parseInt(d[0]) ;
            const m = parseInt(d[1]) ;
            const j = parseInt(d[2]) + parseInt(intDays)  ;
            const finalDate = new Date(y,  m , j) 
            const str_day = finalDate.getDate()+" " + months[finalDate.getMonth()-1]+" " + finalDate.getFullYear() ;
            return str_day;
        }



       $(document).on('click', '.this_nav', function(){ 

            var whichButton = $(this).data('nav'); 
            const nfday = $("#this_first_day_week").val() ;
            const nlday = $("#this_last_day_week").val() ;
 
            if (whichButton === 'next') {

                var this_new_first = addDaysToDate( nfday ,7);
                var this_new_last  = addDaysToDate( nlday,7);
                var str_this_new_first = this_new_first.split("-")[2];
                var str_this_new_last  = str_addDaysToDate( nlday,7);

                var delta_scrollTop =  100 ;

            } else if (whichButton === 'prev') {

                var this_new_first = addDaysToDate( nfday,-7);
                var this_new_last  = addDaysToDate( nlday,-7);
                var str_this_new_first = this_new_first.split("-")[2];
                var str_this_new_last  = str_addDaysToDate( nlday,-7);
                var delta_scrollTop =   - 100 ;

            }

            const this_new_scrollTop = parseInt($("#this_scrollTop").val()) + delta_scrollTop ;
            $('#edt_listing_text').animate({ scrollTop: this_new_scrollTop },'slow');

            $("#this_scrollTop").val(this_new_scrollTop) ;
            $("#to_fill_this_slot_week").html("Semaine du "+str_this_new_first+" au "+str_this_new_last) ;
            $("#this_first_day_week").val(this_new_first);
            $("#this_last_day_week").val(this_new_last);

            length = $(".class_days").length;

            for(let i=0;i<length;i++){ 
                $("#day"+i).html(parseInt(str_this_new_first)+i);
            }


        });



       $('body').on('click', '.fill_edt_this_slot' , function(){  

            const this_first_day_week = $("#this_first_day_week").val();
            const this_details = $(this).data('slot').split("-");
            const slot  = this_details[0] ;
            const day = this_details[1] ;
            const ndate  = addDaysToDate(this_first_day_week, day)

            $("#to_fill_this_slot_day").val(ndate)
            $("#to_fill_this_slot_slot").val(slot)

            const months = ['Jan.','Fev.','Mars','Avr.','Mai','Juin','Juil.', 'Aout','Sept.','Oct.','Nov.', 'Déc.']
            str_day = ndate.split("-")
            str_ndate = str_day[2]+" " + months[parseInt(str_day[1])-1] +" " + str_day[0] ;

            $("#fill_this_slot_day").html(str_ndate);
            $("#fill_this_slot_slot").html(slot);   

        });

        if ($("#id_content")){

            CKEDITOR.replace('content', {
                height: '200px' ,
                toolbar:    
                    [  
                        { name: 'paragraph',  items: [ 'NumberedList', 'BulletedList', '-',   'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock' ] }, 
                        { name: 'basicstyles',  items: [ 'Bold', 'Italic', 'Underline','-','TextColor', 'BGColor'  ] },
                        { name: 'insert', items: [ 'Table', 'HorizontalRule']},
                    ] ,
            });
        }



        $(document).on('click', '.insert_this_into_edt' , function(){ 

            const id   = $(this).data('id') ;
            const type = $(this).data('type') ;
            const title   = $(this).data('title') ;
            const mg = CKEDITOR.instances.id_content.getData() ;            
            
            if ( mg.includes(type) ){ 
                if (type=="Savoir Faire"){
                    msg = mg + title 
                }
                else{
                    msg = mg.trim().substring(3,mg.length-5) + ", "+ title 
                }
                
            }
            else {
               msg = mg + "<strong>"+ type +" </strong> : "+title 
            } 

            CKEDITOR.instances['id_content'].setData(msg) ; 

        });


    });
});        