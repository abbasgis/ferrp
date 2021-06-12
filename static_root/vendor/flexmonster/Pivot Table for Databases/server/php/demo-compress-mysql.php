<?php

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods', 'OPTIONS,GET,PUT,POST,DELETE');
header('Access-Control-Allow-Headers', 'Content-Type');
header('Content-Type: text/plain');

$server = "localhost";
$username = "user";
$password = "password";
$dbname = "foodmart";
mysql_connect($server, $username, $password);
mysql_select_db($dbname);
$result = mysql_query("SELECT * FROM customer");

require_once("flexmonster-compressor.php");
Compressor::compressMySql($result);

mysql_free_result($result);

?>