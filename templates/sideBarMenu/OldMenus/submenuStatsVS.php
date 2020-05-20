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
       <?PHP if (in_array("default", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=tdb_fullpage_default_vs"><i class="fa fa-dashboard"></i>Tableau de bord</a></li>  
      <?PHP if ($_GET['idt']==1) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=fullpage_tdb_absence_index&idt=1"><i class="fa fa-user-times"></i>Absences</a></li>
       <?PHP if ($_GET['idt']==2) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=fullpage_tdb_absence_index&idt=2"><i class="fa fa-clock-o"></i>Retards</a></li>              
       <?PHP if ($_GET['idt']==4) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=fullpage_tdb_absence_index&idt=4"><i class="fa fa-heartbeat"></i>Infirmerie</a></li>         
       <?PHP if ($_GET['idt']==5) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=fullpage_tdb_absence_index&idt=5"><i class="fa fa-legal"></i>Sanctions</a></li>
      <?PHP if (in_array("letter", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=fullpage_tdb_absence_index&idt=6"><i class="fa fa-ticket"></i>Dispenses</a></li>

       <?PHP if (in_array("schedule", $tab)) { echo"<li class='active line-up'>";} else { echo"<li class='line-up'>";}?> <a href="?to=vs_tdb_schedule_group_fullpage"><i class="fa fa-calendar"></i>Edt des groupes</a></li> 
        <?PHP if (in_array("group", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?> <a href="?to=vs_tdb_group_index_fullpage"><i class="fa fa-users"></i>Groupes </a></li> 
        <?PHP if (in_array("classroom", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=vs_tdb_classroom_index_fullpage"><i class="fa fa-sitemap"></i><span>Classes</span></a></li>  
        <?PHP if ((in_array("studentIndex", $tab)) || 
                  (in_array("studentNew", $tab)) || 
                  (in_array("studentEdit", $tab)) || (in_array("studentCsv", $tab))  ) { echo"<li class='active'>";} else { echo"<li>";}?> <a href="?to=vs_tdb_user_studentIndex_fullpage"><i class="fa fa-mortar-board"></i>Eleves</a></li>        
        <?PHP if ((in_array("teacherIndex", $tab)) || 
                  (in_array("teacherNew", $tab)) || 
                  (in_array("teacherEdit", $tab)) || (in_array("teacherCsv", $tab)) || (in_array("teachers", $tab)) )
          { echo"<li class='active'>";} else { echo"<li>";}?> <a href="?to=vs_tdb_user_teacherIndex_fullpage"><i class="fa fa-user"></i>Enseignants</a></li> 
       <?PHP if ($_GET['idt']==3) { echo"<li class='active'>";} else { echo"<li>";}?><a href="?to=fullpage_tdb_absence_index&idt=3"><i class="fa fa-home"></i>Devoirs non faits</a></li>                               
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






      <?PHP if (in_array("bulletin", $tab)) { $activ ='active' ;} else { $activ ='';}?>
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
                     echo"<a href='?to=vs_fullpage_bulletin_indexVsEleve&name=$name&id=$id'><i class='fa fa-newspaper-o'></i>  $name</a></li>" ; 
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
