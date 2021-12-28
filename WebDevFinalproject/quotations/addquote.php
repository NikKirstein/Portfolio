<!DOCTYPE html>
<!-- 
Allow the user to enter a year to see all data base 
records that were released in that year or later

Author: Esme Middaugh and Nik Kirstein
-->

<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<title>Quotation Service</title>
  <link rel="stylesheet" type="text/css" href="style.css">
  <link href="https://fonts.googleapis.com/css?family=Open+Sans|Bungee+Shade" rel="stylesheet">

</head>

<div class="container">
<h2> Quotations</h2>


    <div class="nav">

    <?php
    if (!isset ( $_SESSION ['user'] )) {
    ?>
            <a href="login.php" class="headerButtons">Login</a>
            <a href="login.php" class="headerButtons">Register</a>
    <?php } ?>
    
    <?php
    if (isset ( $_SESSION ['user'] )) {
        echo '<br>Hello ' . $_SESSION ['user'];
    ?>
    <form action="controller.php" method="post">
        &nbsp;&nbsp; <input type="submit" name="action" value="Logout">
    </form>
    <?php } ?>
    
    <a href="addquote.php" class="headerButtons"/>Add Quote</a>

    </div>
    
    <h4>Add a Quote and other users can upvote or downvote it!</h4>
    <div class="formFill">
    	<form method="post" action="controller.php">
		    <label>Quote:</label><input type="textarea" wrap="soft" rows="4" cols="50" name="quoteToAdd"/>
		    <br>
		    <label>Author:</label><input tpye="text" name="authorToAdd"/>
		    <br> <br>
		    <input type="submit" class="adjuster" value="Add Quote"/>
    	</form>
    

	</div>
</body>
</html>




