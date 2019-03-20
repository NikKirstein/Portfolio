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
<body onload="getQuotes()">

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
	<br>
	<div id="toChange"></div>

	<script>
		var divToChange = document.getElementById("toChange");
		function getQuotes() {
			var anObj = new XMLHttpRequest();
			//var actor = document.getElementById("actRole").value;
			anObj.open("GET", "controller.php", true);
			anObj.send();

			anObj.onreadystatechange = function() {
				if (anObj.readyState == 4 && anObj.status == 200) {
					var array = JSON.parse(anObj.responseText);
					var str = "";
					for (i = 0; i < array.length; i++){
						var quote = array[i]['quote'];
						var id = array[i]['id'];
						var rating = array[i]['rating'];
						var flag  = array[i]['flagged'];
						str += "<div class='quote' id='" + id + "''><span class='q'>\"" + quote + "\"</span><br>  <div class='a'> &mdash;" + array[i]['author'] + " <br> <input type='button' class='adjuster'  value='+' onclick='increaseRating(" + id +  ")'/>" + 
					rating +
					"<input type='button' class='adjuster' value='-' onclick='decreaseRating(" + array[i]['id'] + ")'/>"+ 
					"<input type='button' class='adjuster' value='Flag' onclick='flagQuote(" + array[i]['id'] + ")'/>"
								+ "</div></div>";
					//divToChange.innerHTML = str;
				}
				divToChange.innerHTML = str;
			}
			
		}}

		function increaseRating(ids){
			var divToChange = document.getElementById("toChange");
			var anObj = new XMLHttpRequest();
			//var actor = document.getElementById("actRole").value;
			anObj.open("GET", "controller.php?increase=" + ids, true);
			anObj.send();
			anObj.onreadystatechange = function() {
				if (anObj.readyState == 4 && anObj.status == 200) {
					var array = JSON.parse(anObj.responseText);
					var str = "";
					for (i = 0; i < array.length; i++){
						var quote = array[i]['quote'];
						var id = array[i]['id'];
						var rating = array[i]['rating'];
						var flag  = array[i]['flagged'];
						str += "<div class='quote' id='" + id + "''><span class='q'>\"" + quote + "\"</span><br>  <div class='a'> &mdash;" + array[i]['author'] + " <br> <input type='button' class='adjuster'  value='+' onclick='increaseRating(" + id +  ")'/>" + 
					rating + 
					"<input type='button' class='adjuster' value='-' onclick='decreaseRating(" + array[i]['id'] + ")'/>"+ 
					"<input type='button' class='adjuster' value='Flag' onclick='flagQuote(" + array[i]['id'] + ")'/>"
								+ "</div></div>";
					//divToChange.innerHTML = str;
				}
				divToChange.innerHTML = str;
			}
			
		}}
			

		function decreaseRating(ids){
			var divToChange = document.getElementById("toChange");
			var anObj = new XMLHttpRequest();
			//var actor = document.getElementById("actRole").value;
			anObj.open("GET", "controller.php?decrease=" + ids, true);
			anObj.send();
			anObj.onreadystatechange = function() {
				if (anObj.readyState == 4 && anObj.status == 200) {
					var array = JSON.parse(anObj.responseText);
					var str = "";
					for (i = 0; i < array.length; i++){
						var quote = array[i]['quote'];
						var id = array[i]['id'];
						var rating = array[i]['rating'];
						var flag  = array[i]['flagged'];
						str += "<div class='quote' id='" + id + "''><span class='q'>\"" + quote + "\"</span><br>  <div class='a'> &mdash;" + array[i]['author'] + " <br> <input type='button' class='adjuster'  value='+' onclick='increaseRating(" + id +  ")'/>" + 
					rating + 
					"<input type='button' class='adjuster' value='-' onclick='decreaseRating(" + array[i]['id'] + ")'/>"+ 
					"<input type='button' class='adjuster' value='Flag' onclick='flagQuote(" + array[i]['id'] + ")'/>"
								+ "</div></div>";
					//divToChange.innerHTML = str;
				}
				divToChange.innerHTML = str;
			}
			
		}}

		function flagQuote(ids){
			var divToChange = document.getElementById("toChange");
			var anObj = new XMLHttpRequest();
			//var actor = document.getElementById("actRole").value;
			anObj.open("GET", "controller.php?flagged=" + ids, true);
			anObj.send();
			anObj.onreadystatechange = function() {
				if (anObj.readyState == 4 && anObj.status == 200) {
					var array = JSON.parse(anObj.responseText);
					var str = "";
					for (i = 0; i < array.length; i++){
						var quote = array[i]['quote'];
						var id = array[i]['id'];
						var rating = array[i]['rating'];
						var flag  = array[i]['flagged'];
						str += "<div class='quote' id='" + id + "''><span class='q'>\"" + quote + "\"</span><br>  <div class='a'> &mdash;" + array[i]['author'] + " <br> <input type='button' class='adjuster'  value='+' onclick='increaseRating(" + id +  ")'/>" + 
					rating + 
					"<input type='button' class='adjuster' value='-' onclick='decreaseRating(" + array[i]['id'] + ")'/>"+ 
					"<input type='button' class='adjuster' value='Flag' onclick='flagQuote(" + array[i]['id'] + ")'/>"
								+ "</div></div>";
					//divToChange.innerHTML = str;
				}
				divToChange.innerHTML = str;
			}
			
		}}

	</script>

</div>
</body>
</html>




