<ul class="sidebar-menu admin-menu">
      
     

        <?PHP if (in_array("compte", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>
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


        <?PHP if (in_array("socle", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>
          <a href="#" data-target-id="socle">
            <i class="fa fa-briefcase fa-2x"></i> 
            <div class="captionmenu">Socle</div>
          </a>
        </li>


        <?PHP if (in_array("general", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>
          <a href="#" data-target-id="etablissements">
            <i class="fa fa-university fa-2x"></i> 
            <div class="captionmenu">Etablissements</div>
          </a>
        </li>


        <?PHP if (in_array("admindistance", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>
          <a href="#" data-target-id="support">
            <i class="fa fa-support fa-2x"></i> 
            <div class="captionmenu">Support</div>
          </a>
        </li>


        <?PHP if (in_array("mail", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>
          <a href="#" data-target-id="courriel">
            <i class="fa fa-inbox fa-2x"></i> 
            <div class="captionmenu">Courriel</div>
          </a>
        </li>
      </ul>  