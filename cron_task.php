<?php
$servername = "localhost";
$username = "username";
$password = "password";
$dbname = "myDB";

$today = getdate() ;
// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}
 

$sql = "UPDATE qcm_parcours SET is_publish=0 WHERE stop < $today ";

$conn->query($sql) ;
$conn->close();
?>


 