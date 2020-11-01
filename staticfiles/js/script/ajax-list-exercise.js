define(['jquery', 'bootstrap', 'config_toggle'], function ($) {
    $(document).ready(function () {
 

        try {
          $('[data-toggle="popover"]').popover();
        }
        catch(err) {
          console.log("popover not load") ;
        }

 
    });
});