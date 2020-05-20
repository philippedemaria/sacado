<?PHP 
$sommen = 0 ;
$datan = mysql_fetch_array(mysql_query("SELECT * FROM install WHERE id = '1' "));
for($n=1;$n<=13;$n++)
{
$sommen = $sommen + $datan[$n];
}
if ($sommen == 13)
{
?>



<style>
  #sidebar{
    width: 100%; height: 600px; overflow: hidden;
  }
  #scroller{
      width: 110%; height: 100%; overflow-y: scroll;  padding-right: 10%; 
  }

   .trimestre1{ 
  width:50px;
  text-align:center;
  }

  .trimestre2{ 
  width:50px;
  text-align:center;
  background: #f5f5f5;
  }

  .trimestre3{ 
  width:50px;
  text-align:center;
  } 
  ::-webkit-scrollbar { display: none; }
</style>      


   <?PHP if ((in_array("tdb", $tab)) || (in_array("letter", $tab))) { $activ ='active' ;} else { $activ ='';}?>
   <div class="admin-content <?PHP echo $activ ; ?>" id="tdb">
       <ul class="nav nav-pills nav-stacked">
         <?PHP if (in_array("default", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=tdb_fullpage_default_admin"><i class="fa fa-dashboard"></i>Tableau de bord</a></li>          

          
          <?PHP if (in_array("bulletin", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=admin_tdb_bulletin_order"><i class="fa fa-newspaper-o"></i> Bulletin</a></li>      
          <?PHP if (in_array("classroom", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=admin_tdb_classroom_index"><i class="fa fa-sitemap"></i><span>Classes</span></a></li>  
          <?PHP if ((in_array("teacherIndex", $tab)) || 
                    (in_array("teacherNew", $tab)) || 
                    (in_array("teacherEdit", $tab)) || (in_array("teacherCsv", $tab)) || (in_array("teachers", $tab)) )
            { echo"<li class='active'>";} else { echo"<li>";}?> <a href="?to=admin_tdb_user_teacherIndex"><i class="fa fa-user"></i>Enseignants</a></li>                      
          <?PHP if ((in_array("studentIndex", $tab)) || 
                    (in_array("studentNew", $tab)) || 
                    (in_array("studentEdit", $tab)) || (in_array("studentCsv", $tab))  ) { echo"<li class='active'>";} else { echo"<li>";}?> <a href="?to=admin_tdb_user_studentIndex"><i class="fa fa-mortar-board"></i>Eleves</a></li>
           <?PHP if (in_array("user", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?> <a href="?to=admin_tdb_user_index"><i class="fa fa-square"></i>Communauté</a></li>                       
          <?PHP if (in_array("group", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?> <a href="?to=admin_tdb_group_index"><i class="fa fa-users"></i>Groupes </a></li> 
         <?PHP if (in_array("schedule", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?> <a href="?to=admin_tdb_schedule_index"><i class="fa fa-calendar"></i>Emploi du temps</a></li> 
         <?PHP if (in_array("letter", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=admin_letter_letterAdmin_index"><i class="fa fa-pencil"></i>Courrier administratif</a></li>
      </ul>
    </div>


   <?PHP if (in_array("compte", $tab)) { $activ ='active' ;} else { $activ ='';}?>
   <div class="admin-content <?PHP echo $activ ; ?>" id="compte">
      <ul class="nav nav-pills nav-stacked">
          <li><a><span class="blue"><?PHP echo $_SESSION['user_firstname']." ".$_SESSION['user_lastname'] ; ?></span></a></li>         
          <li><a href="?to=teacher_user_profile_view"><img src="../public/img/sacado-icon.png" border="0" width="15px"/> Mon compte</a> </li>
            <?PHP include('AccessByRole.php') ; ?>
          <li><a href="./session/deconnexion.php"> <i class="fa fa-sign-out"></i>      Déconnexion</a></li>
      </ul>
    </div>


   <?PHP if (in_array("school", $tab)) { $activ ='active' ;} else { $activ ='';}?>
   <div class="admin-content <?PHP echo $activ ;?>" id="etablissements">
      <ul class="nav nav-pills nav-stacked">
          <?PHP if (in_array("schooldata", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=admin_school_schooldata_index"><i class="fa fa-university"></i> <span>Données</span></a></li>
          <?PHP if (in_array("period", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=admin_school_period_index"><i class="fa fa-flag-o"></i>Périodes</a></li>            
          <?PHP if (in_array("schoollevel", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=admin_school_schoollevel_index"><i class="fa fa-puzzle-piece"></i> <span>Niveaux</span></a></li>
          <?PHP if ((in_array("schoolsubject", $tab))||(in_array("schoolsubjectlevel", $tab)) ) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=admin_school_schoolsubject_index"><i class="fa fa-laptop"></i> <span>Enseignements</span></a></li>
          <?PHP if (in_array("subjectcoeff", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?> <a href="?to=admin_school_subjectcoeff_index"><i class="fa fa-link"></i>Coefficients </a></li> 
          
          <?PHP /* if (in_array("userassociated", $tab)) { echo"<li class='active'>";} else { echo"<li>";} */?> <!-- <a href="?to=admin_school_userassociated_index"><i class="fa fa-plug"></i>Enseignant/Classe </a></li> -->

         
          <?PHP if (in_array("room", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=admin_school_room_index"><i class="fa fa-key"></i>Salles</a></li>            
          <?PHP if (in_array("time", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=admin_school_time_index"><i class="fa fa-clock-o"></i>Horaires</a></li>
                         
          <?PHP if (in_array("holiday", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=admin_school_holiday_index"><i class="fa fa-plane"></i>Vacances</a></li>                   
      </ul>
    </div>


   <?PHP if (in_array("socle", $tab)) { $activ ='active' ;} else { $activ ='';}?>
   <div class="admin-content <?PHP echo $activ ;?>" id="socle">
      <ul class="nav nav-pills nav-stacked">
          <?PHP if (in_array("itemstage", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>
                <a href="?to=admin_socle_itemstage_index"><i class="fa fa-tags"></i> Acquisition des compétences</a>
          </li>
          <?PHP if (in_array("knowledgestage", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>
                <a href="?to=admin_socle_knowledgestage_index"><i class="fa fa-wrench"></i> Acquisition des savoirs</a> 
          </li>
          <?PHP if (in_array("evaluationdata", $tab)) { echo"<li class='active'>";} else { echo"<li>";} 

              $n = mysql_num_rows(mysql_query("SELECT * FROM evaluationdata WHERE school_id='".$_SESSION['school_id']."'  "));
              if ($n > 0) {?>
             <a href="?to=admin_socle_evaluationdata_index"><i class="fa fa-info-circle"></i> <span>Niveaux d'acquisition</span></a>
             <?PHP } else { ?>
             <a href="?to=admin_socle_evaluationdata_new"><i class="fa fa-info-circle"></i> <span>Niveaux d'acquisition</span></a>
             <?PHP }  ?>
          </li>              
      </ul>
    </div>

      <?PHP if (in_array("indexAdmin", $tab)) { $activ ='active' ;} else { $activ ='';}?>
      <div class="admin-content  <?PHP echo $activ ; ?>" id="bulletin">  
      <div id="sidebar">
        <div id="scroller"> 
              <ul class="nav nav-pills nav-stacked"> 

                <?PHP  $sch = $_SESSION['school_id'];  $year = $_SESSION['this_year'];

                  $req = mysql_query("SELECT name,id FROM classroom WHERE year = '$year' ");
                  while($ligne=mysql_fetch_assoc($req))
                  {
                    $name = stripslashes($ligne['name']); 
                    $id = $ligne["id"];    
                     if (isset($_GET['name']) )
                        {
                     if ($_GET['name'] == $name) { echo"<li class='active'>";} else { echo"<li>";} 
                        }
                        else { echo"<li>";} 
                     echo"<a href='?to=admin_fullpage_bulletin_indexAdmin&name=$name&id=$id'><i class='fa fa-newspaper-o'></i>  $name</a></li>" ; 
                  } 
                ?> 
              
              </ul>

        </div>
      </div>
    </div>



<div class="admin-content" id="courriel">
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
<?PHP } ?>
