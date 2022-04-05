<?php
require_once( dirname(__FILE__). '/logging.php');

if ($_GET["word"] != null) {
    $cnt = accessDB("SEARCH", $_GET["word"]);

    if($cnt > 0){
        accessDB("ADD", $_GET["word"], $cnt+1);
    }
    else{
        accessDB("NEW", $_GET["word"]);
    }
}
?>