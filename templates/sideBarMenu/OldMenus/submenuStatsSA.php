       <?PHP if (in_array("tdb", $tab)) { $activ ='active' ;} else { $activ ='';}?>
       <div class="admin-content <?PHP echo $activ ; ?>" id="tdb">
           <ul class="nav nav-pills nav-stacked">
             <?PHP if (in_array("tdb", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=tdb_fullpage_default_creator"><i class="fa fa-dashboard"></i>Tableau de bord</a></li>          
          </ul>
        </div>


	  <?php print_r($_SESSION);?>
       <?PHP if (in_array("compte", $tab)) { $activ ='active' ;} else { $activ ='';}?>
       <div class="admin-content <?PHP echo $activ ; ?>" id="compte">
          <ul class="nav nav-pills nav-stacked">
              <li><a><span class="blue"><?PHP echo $_SESSION['user_firstname']." ".$_SESSION['user_lastname'] ; ?></span></a></li>         
              <li><a href="?to=teacher_user_profile_view"><img src="../public/img/sacado-icon.png" border="0" width="15px"/> Mon compte</a> </li>
              <?PHP include ("AccessByRole.php") ?>
             <li><a href="./session/deconnexion.php"> <i class="fa fa-sign-out"></i>      Déconnexion</a></li>
          </ul>
        </div>



       <?PHP if (in_array("socle", $tab)) { $activ ='active' ;} else { $activ ='';}?>
       <div class="admin-content <?PHP echo $activ ; ?>" id="socle">    
              <ul class="nav nav-pills nav-stacked ">      
                  <?PHP if (in_array("cycle", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=creator_socle_cycle_index"><i class="fa fa-repeat"></i> Cycles</a></li>              
                  <?PHP if (in_array("domain", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=creator_socle_domain_index"><i class="fa fa-tags"></i> Domaines</a></li>
                  <?PHP if (in_array("competency", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=creator_socle_competency_index"><i class="fa fa-list"></i> Compétences</a></li>
                  <?PHP if (in_array("item", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=creator_socle_item_index"><i class="fa fa-tag"></i> Items</a></li>            
                  <?PHP if (in_array("theme", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=creator_socle_theme_index"><i class="fa fa-reorder"></i> Thèmes</a></li>
                  <?PHP if (in_array("waiting", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=creator_socle_waiting_index"><i class="fa fa-thumb-tack"></i> Attendus</a></li>
                  <?PHP if (in_array("knowledge", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=creator_socle_knowledge_index"><i class="fa fa-wrench"></i> Savoirs</a></li>                  
              </ul>
        </div>





       <?PHP if (in_array("general", $tab)) { $activ ='active' ;} else { $activ ='';}?>
       <div class="admin-content <?PHP echo $activ ; ?>" id="etablissements">        
          <ul class="nav nav-pills nav-stacked">
              <?PHP if (in_array("school", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>
              <a href="?to=creator_general_school_index"><i class="fa fa-university"></i> Etablissement
                      <?PHP if (mysql_num_rows(mysql_query("SELECT * FROM sacado_commun.school WHERE accept='0' ")) > 0 ) { ?>
                      <span class="pull-right-container">
                            <small class="label pull-right bg-yellow"><?PHP  echo mysql_num_rows(mysql_query("SELECT * FROM sacado_commun.school WHERE accept='0' ")); ?></small>
                      </span>
                      <?PHP } ?>
                  </a>
              </li>
              <?PHP if (in_array("level", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=creator_general_level_index"><i class="fa fa-list-ol"></i> Niveaux</a> </li>
              <?PHP if (in_array("subject", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=creator_general_subject_index"><i class="fa fa-laptop"></i> Enseignements</a></li>
          </ul>
        </div>





       <?PHP if (in_array("admindistance", $tab)) { $activ ='active' ;} else { $activ ='';}?>
       <div class="admin-content <?PHP echo $activ ; ?>" id="support">  
          <ul class="nav nav-pills nav-stacked">
              <li><a href="?to=creator_admindistance_default_admindistance"><i class="fa fa-clone"></i>Administrer à distance</a></li>
          </ul>                
        </div>



       <?PHP if (in_array("courriel", $tab)) { $activ ='active' ;} else { $activ ='';}?>
       <div class="admin-content <?PHP echo $activ ; ?>" id="courriel">
          <ul class="nav nav-pills nav-stacked">
            <li>
              <a href="pages/mailbox/mailbox.html">
               <i class="fa fa-envelope"></i> <span>Mailbox</span>
                <span class="pull-right-container">
                  <small class="label pull-right bg-yellow">12</small>
                  <small class="label pull-right bg-green">16</small>
                  <small class="label pull-right bg-red">5</small>
                </span>
              </a>
           </li>
          </ul> 
        </div>