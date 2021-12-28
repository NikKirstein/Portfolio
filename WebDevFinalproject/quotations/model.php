 <?php
// Author: Esme Middaugh and Nik Kirstein
//
class DatabaseAdaptor {
  // The instance variable used in every one of the functions in class DatbaseAdaptor
  private $DB;
  // Make a connection to an existing data based named 'imdb_small' that has
  // table . In this assignment you will also need a new table named 'users'
  public function __construct() {
    $db = 'mysql:dbname=quotations;host=127.0.0.1;charset=utf8';
    $user = 'root';
    $password = '';
    
    try {
      $this->DB = new PDO ( $db, $user, $password );
      $this->DB->setAttribute ( PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION );
    } catch ( PDOException $e ) {
      echo ('Error establishing Connection');
      exit ();
    }
  }
 
//EVERYTHING IN THIS FILE NEEDS $stmt->bindParam() THING as well as the htmlspecialchars($text); thing (I dont even know where that goes?).  Its required in spec
//Code from the project page. Not sure what it does 
  public function getAllQuotes () {
   $stmt = $this->DB->prepare ( "SELECT * FROM quotes WHERE flagged !=1 ORDER BY rating DESC");
   $stmt->execute ();
   return $stmt->fetchAll ( PDO::FETCH_ASSOC );
  }

  public function increaseRating($id){
   //$update = '"UPDATE quotes SET rating=' . "'Doe'" .  'WHERE id=' . $id . '"'
   $stmt = $this->DB->prepare ( "UPDATE quotes SET rating = rating + 1 WHERE id = ". (int)$id);
   $stmt->execute ();
   $stmt = $this->DB->prepare ( "SELECT * FROM quotes WHERE flagged !=1 ORDER BY rating DESC");
   $stmt->execute ();
   return $stmt->fetchAll ( PDO::FETCH_ASSOC );
  }
	
  public function decreaseRating($id){
	   //$update = '"UPDATE quotes SET rating=' . "'Doe'" .  'WHERE id=' . $id . '"'
   $stmt = $this->DB->prepare ( "UPDATE quotes SET rating = rating - 1 WHERE id = ". (int)$id);
   $stmt->execute ();
   $stmt = $this->DB->prepare ( "SELECT * FROM quotes WHERE flagged !=1 ORDER BY rating DESC");
   $stmt->execute ();
   return $stmt->fetchAll ( PDO::FETCH_ASSOC );
  }
	
  public function flag($id){
   $stmt = $this->DB->prepare ( "UPDATE quotes SET flagged=1 WHERE id = ". (int)$id);
   $stmt->execute ();
   $stmt = $this->DB->prepare ( "SELECT * FROM quotes WHERE flagged !=1 ORDER BY rating DESC");
   $stmt->execute ();
   return $stmt->fetchAll ( PDO::FETCH_ASSOC );
  }
	
  public function addQuote($quote, $author){
		//$update = '"UPDATE quotes SET rating=' . "'Doe'" .  'WHERE id=' . $id . '"'
   $stmt = $this->DB->prepare ( "INSERT INTO quotes(quote, author, rating, flagged) values('" . $quote . "','" .  $author . "', 0,0)");
   $stmt->execute ();
   $stmt = $this->DB->prepare ( "SELECT * FROM quotes WHERE flagged !=1 ORDER BY rating DESC");
   $stmt->execute ();
   return $stmt->fetchAll ( PDO::FETCH_ASSOC );
  }
	
  public function checkUserExist($uname) {
   $stmt = $this->DB->prepare ( "SELECT Username FROM users" );
   $stmt->execute ();
   $checkArr = $stmt->fetchAll ( PDO::FETCH_ASSOC );
   return $stmt->fetchAll ( PDO::FETCH_ASSOC );
	//return in_array($uname, $checkArr);
  }
	
  public function registerNew($Username, $pass) {
   $stmt = $this->DB->prepare ( "INSERT INTO users values ( " . $Username . "," . $pass . ")"); //does  this account for the ID?
   $stmt->execute ();
   return $stmt->fetchAll ( PDO::FETCH_ASSOC );
  }





}
// Testing code that should not be run when a part of MVC
$theDBA = new DatabaseAdaptor ();
// $arr = $theDBA->getAllMoviesAfterYear (2000);
// print_r($arr);
 
?>