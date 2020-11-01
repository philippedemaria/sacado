define(['jquery',  'bootstrap',  'toggle',], function ($) {
    // fonctions pour gérer l'apparition d'un élément quand on clique sur un checkbox (ou toggle) todo:vérifier les anciennces et si elles servent encore

    
    function makeItemAppear($toggle, $item) {
        $toggle.change(function () {
            if ($toggle.is(":checked")) {
                $item.hide(500);
            } else {
                $item.show(500);
            }
        });
    }

  
        try {
          $('[data-toggle="popover"]').popover();
        }
        catch(err) {
          console.log("popover not load") ;
        }
 
  

    function hiddenItem($toggle, $item) {
        $toggle.change(function () {
            if ($toggle.is(":checked")) {
                $item.show(500);
            } else {
                $item.hide(500);
            }
        });
    }

 
});