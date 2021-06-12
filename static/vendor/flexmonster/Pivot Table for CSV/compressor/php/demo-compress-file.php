<?php

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods', 'OPTIONS,GET,PUT,POST,DELETE');
header('Access-Control-Allow-Headers', 'Content-Type');
header('Content-Type: text/plain');

require_once("flexmonster-compressor.php");
Compressor::compressFile("data.csv");

?>