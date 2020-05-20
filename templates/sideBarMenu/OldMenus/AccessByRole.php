<?PHP 

// Super admin = 10
if ($_SESSION['user_role'] == 10) { echo"
                                        <li><a href='changeRole.php?a=10'><i class='fa fa-globe'></i> Super admin</a></li>
                                        <li><a href='changeRole.php?a=9'><i class='fa fa-life-ring'></i> Administrateur</a></li>
                                        <li><a href='changeRole.php?a=4'><i class='fa fa-heartbeat'></i> Infirmerie</a></li>
                                        <li><a href='changeRole.php?a=3'><i class='fa fa-hand-peace-o'></i> Vie scolaire</a></li>
                                        <li><a href='changeRole.php?a=2'><i class='fa fa-user'></i> Enseignant</a></li>
                                        <li><a href='changeRole.php?a=1'><i class='fa fa-mortar-board'></i> Elève</a></li>
                                        <li><a href='changeRole.php?a=0'><i class='fa fa-users'></i> Parent</a></li>                                                                              
                                      " ;  } 

// Admin général = 9
elseif ($_SESSION['user_role'] == 9) { echo"<li><a href='changeRole.php?a=9'><i class='fa fa-life-ring'></i> Administrateur</a></li>
                                        <li><a href='changeRole.php?a=4'><i class='fa fa-heartbeat'></i> Infirmerie</a></li>
                                        <li><a href='changeRole.php?a=3'><i class='fa fa-hand-peace-o'></i> Vie scolaire</a></li>
                                        <li><a href='changeRole.php?a=2'><i class='fa fa-user'></i> Enseignant</a></li>
                                        " ; } 

/* Administration - secrétariat = 5
elseif ($_SESSION['user_role'] == 5){ echo"<li><a href='changeRole.php?a=5'><i class='fa fa-archive'></i> Administration</a></li>
                                           <li><a href='changeRole.php?a=4'><i class='fa fa-heartbeat'></i> Infirmerie</a></li>
                                           <li><a href='changeRole.php?a=3'><i class='fa fa-hand-peace-o'></i> Vie scolaire</a></li>" ; } */
// Infirmerie = 4 
elseif ($_SESSION['user_role'] == 4) { echo"<li><a href='changeRole.php?a=4'><i class='fa fa-heartbeat'></i> Infirmerie</a></li>
                                            <li><a href='changeRole.php?a=3'><i class='fa fa-hand-peace-o'></i> Vie scolaire</a></li>" ; }  

// Vie scolaire = 3
elseif ($_SESSION['user_role'] == 3) { echo"<li><a href='changeRole.php?a=3'><i class='fa fa-hand-peace-o'></i> Vie scolaire</a></li>" ; }  

// Enseignant = 2
elseif ($_SESSION['user_role'] == 2) { echo"<li><a href='changeRole.php?a=2'><i class='fa fa-user'></i> Enseignant</a></li>
                                            <li><a href='changeRole.php?a=1'><i class='fa fa-mortar-board'></i> Elève</a></li>" ; }  

// Eleve = 1
elseif ($_SESSION['user_role'] == 1) { echo"<li><a href='changeRole.php?a=1'><i class='fa fa-mortar-board'></i> Elève</a></li>"  ; } 

// Parent = 0
elseif ($_SESSION['user_role'] == 0) { echo"<li><li><a href='changeRole.php?a=0'><i class='fa fa-users'></i> Parent</a></li>   " ; } 

?>


