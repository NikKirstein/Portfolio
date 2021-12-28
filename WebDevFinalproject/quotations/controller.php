<?php
// This controller acts as the go between the view and the model. 
//
// Author Esme Middaugh and Nik Kirstein
//
require 'model.php';  // for $theDBA, an instance of DataBaseAdaptor
session_start ();
#$year = $_GET['year'];
//$actor = $_GET['actor'];
//$role = $_GET["role"];

if (isset ( $_POST ['action'] ) && $_POST ['action'] === 'Logout') {
	unset($_SESSION['user']); //This wont work yet
	header ( 'Location: index.php' );
}

if (isset ( $_POST ['action'] ) && $_POST ['action'] === 'login') {
	$username = $_POST['username'];
	$password = $_POST['password'];
	if ($theDBA->checkUserExist($username)) { 
		$_SESSION ['user'] = $username;
		header ( 'Location: index.php' );
	}
	else { //if it does not exist
		////send back an error message (how?)
		header ( 'Location: login.php' );
	}
}

if (isset ($_POST ['action'] ) && $_POST['action'] === 'register') {
	$regName = $_POST['username'];
	$regPass = $_POST['password'];
	if (!$theDBA->checkUserExist($regname)) { //checkUserExist function is written but might not work, really just needs to return true of false
		$hashed_pw = password_hash($regPass, PASSWORD_DEFAULT);
		$theDBA->registerNew($regName, $hashed_pw);
	//password_verify($regPass, $hashed_pw)  what do I do with this
	$_SESSION ['user'] = $regName; //logs in the person
	header ( 'Location: index.php' );
	}
	else {
		////send back an error message (how?)
		header ( 'Location: login.php' );
	}
}


$arrQuotes = $theDBA->getAllQuotes ();
$toEcho = array();
/*
for ($i=0; $i<count($arrQuotes); $i++){
    $toEcho.push("<div class='quote'>" . array[i]['quote'] . "<br>--\t" . array[i]['quote']

}*/

if (isset($_GET["increase"])){
       $id = $_GET['increase'];
       $arrQuotes = $theDBA->increaseRating($id);

    }
if (isset($_GET["decrease"])){
   $id = $_GET['decrease'];
   $arrQuotes = $theDBA->decreaseRating($id);
    }

if (isset($_GET["flagged"])){
    $id = $_GET['flagged'];
   $arrQuotes = $theDBA->flag($id);
    }

if (isset($_POST["quoteToAdd"])){
	$quote = $_POST['quoteToAdd'];
	$author = $_POST['authorToAdd'];
	$theDBA->addQuote($quote, $author);
	header('Location: index.php');
}
    

echo  json_encode($arrQuotes);


?>