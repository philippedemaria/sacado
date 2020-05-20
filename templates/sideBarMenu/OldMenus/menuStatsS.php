  <ul class="sidebar-menu admin-menu">


      
        <?PHP if (in_array("user", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>
          <a href="#" data-target-id="compte">
            <i class="fa fa-user fa-2x"></i> 
            <div class="captionmenu">Compte</div>
          </a>
        </li>

        <?PHP if (in_array("tdb", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>        
          <a href="#" data-target-id="tdb">
            <i class="fa fa-dashboard fa-2x"></i><br>
            <span class="captionmenu">Tableau de bord</span>
          </a>
        </li>



        <?PHP if (in_array("course", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>      
          <a href="#" data-target-id="cours">
            <i class="fa fa-folder-open fa-2x"></i> 
            <div class="captionmenu">Ressources</div>
          </a>
        </li>



        <?PHP if (in_array("mail", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>       
          <a href="#" data-target-id="courriel">
            <i class="fa fa-inbox fa-2x"></i> 
            <div class="captionmenu">Courriel</div>
          </a>
        </li>
  </ul>  