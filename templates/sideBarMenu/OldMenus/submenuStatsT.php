       <?PHP if ((in_array("tdb", $tab)) OR (in_array("calendar", $tab))  OR (in_array("indexMy", $tab))  ) { $activ ='active' ;} else { $activ ='';}?>
      <div class="admin-content <?PHP echo $activ ; ?>" id="tdb">
            <ul class="nav nav-pills nav-stacked">
                <?PHP if (in_array("default", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=tdb_fullpage_default_teacher"><i class="fa fa-dashboard"></i> Tableau de bord </a></li>           
                <?PHP if (in_array("calendar", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=tdb_fullpage_calendar_cdt"><i class="fa fa-calendar"></i> Emplois du temps</a></li>   
                <?PHP if (in_array("group", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=teacher_fullpage_group_indexMy"><i class="fa fa-users"></i>  Mes groupes</a></li>
                <?PHP if (in_array("absence", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=fullpage_tdb_absence_calling"><i class="fa fa-list"></i> Absences</a></li> 
                <li><a href="https://folios.onisep.fr/saml/login?_pre_saml_idp=profacad&_saml_idp=" target="_blank"><img src="../public/img/folios.jpg" border="0" width="160px" height="25px"/> </a></li>                                
            </ul>
       </div>




       <?PHP if (in_array("user", $tab)) { $activ ='active' ;} else { $activ ='';}?>
       <div class="admin-content <?PHP echo $activ ; ?>" id="compte">
          <ul class="nav nav-pills nav-stacked">
              <li><a><span class="blue"><?PHP echo $_SESSION['user_firstname']." ".$_SESSION['user_lastname'] ; ?></span></a></li>         
              <li><a href="?to=teacher_user_profile_view"><img src="../public/img/sacado-icon.png" border="0" width="15px"/> Mon compte</a> </li>
              <?PHP include ("AccessByRole.php") ?>
             <li><a href="./session/deconnexion.php"> <i class="fa fa-sign-out"></i>      Déconnexion</a></li>
          </ul>
        </div>




       <?PHP if (in_array("course", $tab)) { $activ ='active' ;} else { $activ ='';}?>
       <div class="admin-content  <?PHP echo $activ ; ?>" id="cours">      
          <ul class="nav nav-pills nav-stacked">



         <li class="dropdown active">
    <a class="dropdown-toggle" data-toggle="dropdown" href="#">Menu 1
    <span class="caret"></span></a>
    <ul class="dropdown-menu">
      <li><a href="#">Submenu 1-1</a></li>
      <li><a href="#">Submenu 1-2</a></li>
      <li><a href="#">Submenu 1-3</a></li>
    </ul>
  </li> 




            <?PHP if (in_array("progression", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=teacher_course_progression_index"><i class="fa fa-cogs"></i> Progressions</a></li>          
            <?PHP if (in_array("mychapter", $tab)) { echo"<li class='active line-up'>";} else { echo"<li class='line-up'>";}?><a href="?to=teacher_course_mychapter_index"><i class="fa fa-folder-open"></i>Thèmes d'étude</a></li>
            <?PHP if (in_array("mylesson", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=teacher_course_mylesson_index"><i class="fa fa-file-text-o"></i>Fiches notions</a></li>
            <?PHP if ((in_array("exercise", $tab))|| (in_array("question", $tab)) ) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=teacher_course_exercise_index"><i class="fa fa-tablet"></i>Exercices </a></li>
            <?PHP if (in_array("document", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=teacher_course_document_index"><i class="fa fa-floppy-o"></i>Documents</a></li> 



  <li class="dropdown">
    <a class="dropdown-toggle" data-toggle="dropdown" href="#">Menu 1
    <span class="caret"></span></a>
    <ul class="dropdown-menu">
      <li><a href="#">Submenu 1-1</a></li>
      <li><a href="#">Submenu 1-2</a></li>
      <li><a href="#">Submenu 1-3</a></li>
    </ul>
  </li>





          </ul>
        </div>


       <?PHP if (in_array("eval", $tab)) { $activ ='active' ;} else { $activ ='';}?>
       <div class="admin-content  <?PHP echo $activ ; ?>" id="eval">      
          <ul class="nav nav-pills nav-stacked"> 
            <?PHP if (in_array("evaluation", $tab)) { echo"<li>";} else { echo"<li>";}?><a href="?to=teacher_eval_evaluation_index"><i class="fa fa-trophy"></i>Evaluations </a></li>
            <?PHP if (in_array("online", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=eval_course_online_index"><i class="fa fa-laptop"></i>Evaluations en ligne</a></li>        
            <?PHP if (in_array("evalnote", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=teacher_eval_evalnote_index"><i class="fa fa-table"></i>Notes</a></li> 
            <?PHP if (in_array("average", $tab)) { echo"<li class='active'>";} else { echo"<li class='line-up'>";}?><a href="?to=eval_fullpage_reach_average"><i class="fa fa-line-chart"></i>  Statistiques</a></li> 
            <?PHP if (in_array("compt", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=eval_fullpage_reach_compt"><i class="fa fa-database"></i>  Niveaux des compétences</a></li>                 
            <?PHP if (in_array("waiting", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=eval_fullpage_reach_waiting"><i class="fa fa-thumb-tack"></i>  Niveaux des savoirs</a></li>  
          </ul>
        </div>


       <?PHP if (in_array("socle", $tab)) { $activ ='active' ;} else { $activ ='';}?>
       <div class="admin-content <?PHP echo $activ ; ?>" id="socle">    
              <ul class="nav nav-pills nav-stacked ">                  
                  <?PHP if (in_array("domain", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=teacher_socle_showsocle_domain"><i class="fa fa-tags"></i> Domaines</a></li>
                  <?PHP if (in_array("competency", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=teacher_socle_showsocle_competency"><i class="fa fa-list"></i> Compétences</a></li>            
                  <?PHP if (in_array("knowledge", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=teacher_socle_showsocle_knowledge"><i class="fa fa-wrench"></i> Savoirs</a></li>  
                  <?PHP if (in_array("myknowledge", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=teacher_socle_myknowledge_index"><i class="fa fa-wrench"></i> Mes savoirs personnalisés</a></li>
              </ul>
        </div>

       <?PHP if (in_array("mail", $tab)) { $activ ='active' ;} else { $activ ='';}?>
       <div class="admin-content <?PHP echo $activ ; ?>" id="courriel">
       <a type='text' href="?to=mail_fullpage_courriel_compose" class='btn btn-danger white' data-target='#newCourriel' data-whatever='newMessage' style='width:100%;margin-bottom:20px;'/><i class=\"fa fa-pencil\"></i> <strong>Nouveau</strong> </a>
          <ul class="nav nav-pills nav-stacked">
               
                  <?PHP if (in_array("mailbox", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=mail_fullpage_courriel_mailbox"><i class="fa fa-envelope"></i><span> Boite de réception</span>
                <span class="pull-right-container">
                  <small class="label pull-right bg-red">5</small>
                </span>
              </a>
           </li>
            <?PHP if (in_array("sent", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=mail_fullpage_courriel_sent"><i class="fa fa-share"></i> Messages envoyés</a></li>
            <?PHP if (in_array("contact", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=teacher_mail_contact_index"><i class="fa fa-users"></i> Contact</a></li>
          </ul> 
        </div>


        
        <?PHP if (in_array("bulletin", $tab)) { $activ ='active' ;} else { $activ ='';}?>
       <div class="admin-content  <?PHP echo $activ ; ?>" id="bulletin">      
          <ul class="nav nav-pills nav-stacked"> 

            <?PHP  $usr = $_SESSION['user_id'];


              $req = mysql_query("SELECT name,id FROM classroom WHERE profPrincipal_id='$usr' ");
              while($ligne=mysql_fetch_assoc($req))
              {
              $name = stripslashes($ligne['name']); $id = $ligne["id"];    
               if (isset($_GET['name']) )
                  {
               if ($_GET['name'] == $name) { echo"<li class='active'>";} else { echo"<li>";} 
                  }
                  else { echo"<li>";} 
               echo"<a href='?to=teacher_fullpage_bulletin_indexPP&name=$name&id=$id' class='line-up'><i class='fa fa-newspaper-o'></i>  $name [PP]</a></li>" ; 
              }

               echo"<hr>";

              $req = mysql_query("SELECT name, id, subject_id FROM groupe WHERE user_id='$usr' ");

              while($ligne=mysql_fetch_assoc($req))
              {
              $name = stripslashes($ligne['name']); $id = $ligne["id"];   $subject_id = $ligne["subject_id"]; 


               if (isset($_GET['id']) )
                  {
               if ($_GET['id'] == $id && $_GET['name'] == $name) { echo"<li class='active'>";} else { echo"<li>";} /* Cet appel du name dans le Get permet de mettre en subrillance le menu */
                  }
                  else { echo"<li>";} 
               echo"<a href='?to=teacher_fullpage_bulletin_index&name=$name&id=$id '><i class='fa fa-newspaper-o'></i>  $name</a></li>" ; 
              } 
           
 ?> 


          </ul>
        </div>