<!--
Allow the user to enter a year to see all data base
records that were released in that year or later

Author: Esme Middaugh and Nik Kirstein
-->

<!DOCTYPE html>
<html>
<head>
<meta charset="ISO-8859-1">
<title>Login</title>
<link rel="stylesheet" type="text/css" href="style.css">
<link href="https://fonts.googleapis.com/css?family=Open+Sans|Bungee+Shade" rel="stylesheet">
</head>
<body>

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


<h4>Login or Register as a new user</h4>
	<form action="controller.php" method="post">
		<div class="formFill">
			<label>Username:</label><input type="text" name="username" pattern="/^.{4,}$/" required><br>
			<label>Password:</label><input type="password" name="password" pattern="/^.{6,}$/" required> <br>
		</div>
			<input type="button" name="action" value="register" class='adjuster'>
			<input type="button" name="action" value="login" class='adjuster'>
	</form>
</div>

</body>
</html>