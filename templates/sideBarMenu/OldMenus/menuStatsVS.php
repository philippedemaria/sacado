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


        <?PHP if (in_array("indexVsEleve", $tab)) { echo"<li class='active'>";} else { echo"<li>";}?>
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
<?PHP } ?>