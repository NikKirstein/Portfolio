 <?php

// Author: Esme Middaugh (with code from Prof Mercer)
//
class DatabaseAdaptor {
  // The instance variable used in every one of the functions in class DatbaseAdaptor
  private $DB;
  // Make a connection to an existing data based named 'imdb_small' that has
  // table . In this assignment you will also need a new table named 'users'
  public function __construct() {
    $db = 'mysql:dbname=imdb_small;host=127.0.0.1;charset=utf8';
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
 
 
  public function getAllActors ($substring ) {
    if ((preg_match('/\s/',$substring)) == 1) {
        $stringArr = explode(" ", $substring);
        $stmt = $this->DB->prepare ( "SELECT * FROM actors WHERE first_name like '%". ($stringArr[0]) . "%' AND last_name like '%" . ($stringArr[1]) . "%' LIMIT 50");
        $stmt->execute ();
        return $stmt->fetchAll ( PDO::FETCH_ASSOC );
    }
  	else { 
        $stmt = $this->DB->prepare ( "SELECT * FROM actors WHERE first_name like '%"
  			. $substring . "%' OR last_name like '%" . $substring . "%' LIMIT 50");
        $stmt->execute ();
        return $stmt->fetchAll ( PDO::FETCH_ASSOC );
    }
  } 
  
  public function returnMoviesRoles ($substring) {
    $stringArr = explode(" ", $substring);
    if(count($stringArr) > 2) {
        $stmt = $this->DB->prepare ( "SELECT movies.name, actors.first_name, actors.last_name, 
                roles.role FROM actors JOIN roles ON roles.actor_id = actors.id JOIN movies ON roles.movie_id = movies.id WHERE first_name like '%". ($stringArr[0]) . "%' AND last_name like '%" . ($stringArr[2]) . "%'");
    }
    else {
         $stmt = $this->DB->prepare ( "SELECT movies.name, actors.first_name, actors.last_name, 
                roles.role FROM actors JOIN roles ON roles.actor_id = actors.id JOIN movies ON roles.movie_id = movies.id WHERE first_name like '%". ($stringArr[0]) . "%' AND last_name like '%" . ($stringArr[1]) . "%'");
    }
    $stmt->execute ();
    return $stmt->fetchAll ( PDO::FETCH_ASSOC );     
  }


} //Don't delete -- Closing tag for the DatabaseAdaptor

$theDBA = new DatabaseAdaptor ();

 
?>