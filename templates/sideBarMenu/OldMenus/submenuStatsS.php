       <?PHP if (in_array("user", $tab)) { $activ ='active' ;} else { $activ ='';}?>
       <div class="admin-content <?PHP echo $activ ; ?>" id="compte">
          <ul class="nav nav-pills nav-stacked">
              <li><a><span class="blue"><?PHP echo $_SESSION['user_firstname']." ".$_SESSION['user_lastname'] ; ?></span></a></li>         
              <li><a href="?to=teacher_user_profile_view">Mon compte</a> </li>
              <?PHP include ("AccessByRole.php") ?>
             <li><a href="./session/deconnexion.php"> <i class="fa fa-sign-out"></i>      Déconnexion</a></li>
          </ul>
        </div>      



       <?PHP if (in_array("tdb", $tab)) { $activ ='active' ;} else { $activ ='';}?>
      <div class="admin-content <?PHP echo $activ ; ?>" id="tdb">
            <ul class="nav nav-pills nav-stacked">
                <?PHP if (in_array("default", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=tdb_fullpage_default_student"><i class="fa fa-dashboard"></i> Tableau de bord </a></li>
                <?PHP if (in_array("compt", $tab)) { echo"<li class='active'>";} else { echo"<li class='line-up'>";}?><a href="?to=tdb_fullpage_reach_compt"><i class="fa fa-database"></i>  Niveaux de compétence</a></li>                 
                <?PHP if (in_array("waiting", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=tdb_fullpage_reach_waiting"><i class="fa fa-thumb-tack"></i>  Niveaux des savoirs</a></li> 
                <?PHP if (in_array("epi", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=student_tdb_epi_index"><i class="fa fa-compass"></i>  EPI</a></li> 
                <?PHP if (in_array("folios", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="https://folios.onisep.fr/saml/login?_pre_saml_idp=profacad&_saml_idp=" target="_blank"><img src="../public/img/folios.jpg" border="0" width="160px" height="25px"/> </a></li>                                 
            </ul>
       </div>

       <?PHP if (in_array("course", $tab)) { $activ ='active' ;} else { $activ ='';}?>
       <div class="admin-content  <?PHP echo $activ ; ?>" id="cours">      
          <ul class="nav nav-pills nav-stacked">
           <?PHP if (in_array("cdt", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=student_fullpage_calendar_cdt"><i class="fa fa-calendar"></i> Cahier de texte</a></li> 
            <?PHP $col = 1 ;
                $sqlTeaching = mysql_query("SELECT group_id FROM group_user WHERE user_id = '".$_SESSION['user_id']."' ") ;
                while($reqUserByClass = mysql_fetch_array($sqlTeaching))
                  { $group_id =  $reqUserByClass['group_id'] ;
                    $teachId = mysql_fetch_assoc(mysql_query("SELECT subject_id FROM groupe WHERE id='$group_id'  ")) or die(mysql_error());
                    $Nam = mysql_fetch_assoc(mysql_query("SELECT name,color,shortname FROM sacado_commun.subject WHERE id ='".$teachId['subject_id']."'  ")) ;  
                    $colorT =  stripslashes($Nam['color']); 

                    if(strlen($Nam['name'])>26) { $namT =  stripslashes($Nam['shortname']); } else { $namT =  stripslashes($Nam['name']); } 


                    echo"<li><span data-toggle='collapse' data-target='#demo$col' style='color:$colorT'><i class='fa fa-folder-open'></i> $namT</span>
                              <ul id='demo$col' class='collapse'>";
                      $sqlmyChap = mysql_query("SELECT mychapter_id FROM mychapter_group WHERE group_id = '$group_id' ") or die(mysql_error()) ;                              
                      while($selmyChap = mysql_fetch_array($sqlmyChap))
                      { $myChapter_id =  $selmyChap['mychapter_id'] ;
                        $myChap = mysql_fetch_array(mysql_query("SELECT name,id FROM sacado_commun.mychapter WHERE id = '$myChapter_id' AND public='1' AND subject_id='".$teachId['subject_id']."' ")) ;

                          if(strlen($myChap['name'])>=26) { $chaine=substr($myChap['name'],0,26); }  else  { $chaine=$myChap['name']; }                                              
                            echo"<li class='sanspuce5'><a href='?to=fullpage_course_mychapter_visit&id=".$myChap['id']."' style='color:$colorT'>".stripslashes($chaine)."</a></li>" ;
                          }                                                                
                    echo"</ul>
                        </li>";
                  $col++ ;}
            ?>

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


        
