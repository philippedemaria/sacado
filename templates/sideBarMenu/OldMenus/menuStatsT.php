  <ul class="sidebar-menu admin-menu">

      
        <?PHP if (in_array("user", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>
          <a href="#" data-target-id="compte">
            <i class="fa fa-user fa-2x"></i> 
            <div class="captionmenu">Compte</div>
          </a>
        </li>

        <?PHP if ((in_array("tdb", $tab)) OR (in_array("calendar", $tab)) ){ echo"<li class='active'>";} else { echo"<li>";}?>        
          <a href="#" data-target-id="tdb">
            <i class="fa fa-dashboard fa-2x"></i><br>
            <span class="captionmenu">Tableau de bord</span>
          </a>
        </li>


        <?PHP if (in_array("course", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>      
          <a href="#" data-target-id="cours">
            <i class="fa fa-laptop fa-2x"></i> 
            <div class="captionmenu">Cours</div>
          </a>
        </li>

        <?PHP if (in_array("eval", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>      
          <a href="#" data-target-id="eval">
            <i class="fa fa-trophy fa-2x"></i> 
            <div class="captionmenu">Evaluation</div>
          </a>
        </li>


        <?PHP if (in_array("socle", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>              
          <a href="#" data-target-id="socle">
            <i class="fa fa-briefcase fa-2x"></i> 
            <div class="captionmenu">Socle</div>
          </a>
        </li>

        <?PHP if (in_array("bulletin", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>              
          <a href="#" data-target-id="bulletin">
            <i class="fa fa-newspaper-o fa-2x"></i> 
            <div class="captionmenu">Bulletin</div>
          </a>
        </li>




        <?PHP if (in_array("mail", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>       
          <a href="#" data-target-id="courriel">
            <i class="fa fa-inbox fa-2x"></i> 
            <div class="captionmenu">Courriel</div>
          </a>
        </li>
  </ul>  