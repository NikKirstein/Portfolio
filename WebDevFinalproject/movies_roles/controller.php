<?php
// This controller acts as the go between the view and the model. 
//
// Author Nik Kirstein
//
include 'model.php';  // for $theDBA, an instance of DataBaseAdaptor

if(isset($_GET['actor'])) {
	$substrActor = $_GET['actor'];
	$ACTarr = $theDBA->getAllActors ($substrActor);
	echo  json_encode($ACTarr);
}
if(isset($_GET['info'])) {
	$substrinfo= $_GET['info'];
	$ROLarr = $theDBA->returnMoviesRoles ($substrinfo);
	echo json_encode($ROLarr);
}

?>