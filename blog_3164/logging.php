<?php

/**
* prepare DB access
*
* @param string $cmd : "SEARCH","NEW","ADD"
* @param string $word : search word
* @param int $count : number of searches
* @return int $result : "SEARCH" number of searches , "NEW" -1 , "ADD" -1
*
*/

function accessDB($cmd, $word, $count = 0) {
    
    $filePath = "./db_key/counter_key.txt";
    $key = explode(",", file_get_contents($filePath));
    $host = $key[0];
    $user = $key[1];
    $pass = $key[2];
    $dbName = $key[3];
    $dbTable = $key[4];

    try {
        $sql = new PDO(
                    "mysql:dbname=".$dbName.";host=".$host.";charset=utf8;",
                    $user, $pass);
        
        if($cmd == "SEARCH"){
            $result = search($dbTable, $sql, $word);
        }
        elseif($cmd == "NEW"){
            insert($dbTable, $sql, $word);
            $result = -1;
        }
        elseif($cmd == "ADD"){
            update($dbTable, $sql, $word, $count);
            $result = -1;
        }
        else{
            print("cmd error");
            $result = -1;
        }

        $sql = null;
    }
    catch(Exception $e) {
            my_error_log($word, $e->getMessage());
			die();
    }

    return $result;
}

/**
* search word
*
* @param string $table : DB table name
* @param var  $sql : POD object
* @param string $word : search word
* @return int $retval : number of searches
*
*/

function search($table, $sql, $word) {
    $stmti = $sql->prepare('SELECT * FROM '.$table.' WHERE word = :word LIMIT 0, 1;');
    $stmti->bindValue(':word', $word, PDO::PARAM_STR);
    $res = $stmti->execute();
    $err = $stmti->errorInfo();
    $retval = 0;

    if($res and ($err[0] == 00000)){
        $result = $stmti->fetch(PDO::FETCH_ASSOC);
        $retval = $result["cnt"];
    }
    else{
        my_error_log($word, $err[2]);
    }

    $stmti = null;
    return $retval;
}

/**
* insert word
*
* @param string $table : DB table name
* @param var POD $sql : POD object
* @param string $word : search word
*
*/

function insert($table, $sql, $word) {
    $stmti = $sql->prepare('INSERT INTO '.$table.' (word,cnt) VALUES (:word,:count)');
    $stmti->bindValue(':word', $word, PDO::PARAM_STR);
    $stmti->bindValue(':count', 1, PDO::PARAM_INT);
    $stmti->execute();

    $err = $stmti->errorInfo();
    if($err[0]!=00000){
        my_error_log($word, $err[2]);
    }

    $stmti = null;
}

/**
* upadte word counts
*
* @param string $table : DB table name
* @param var POD $sql : POD object
* @param string $word : search word
* @param int $count : number of searches
*
*/

function update($table, $sql, $word, $count) {
    $stmti = $sql->prepare('UPDATE '.$table.' SET cnt = :count WHERE word = :word;');
    $stmti->bindValue(':count', $count, PDO::PARAM_INT);
    $stmti->bindValue(':word', $word, PDO::PARAM_STR);
    $stmti->execute();

    $err = $stmti->errorInfo();
    if($err[0]!=00000){
        my_error_log($word, $err[2]);
    }

    $stmti = null;
}

/**
* upadte word counts
*
* @param string $word : search word
* @param string $errorInfo : error sentences
*
*/

function my_error_log($word, $errorInfo){
    date_default_timezone_set('Asia/Tokyo');
    
    $file_name = "./error/".date("Y_m_d H_i_s");

    $line = $word . " | " . $errorInfo;

    if (!file_exists($file_name)) {
        file_put_contents($file_name.".txt", $line, LOCK_EX);
    }else{
        file_put_contents($file_name."2.txt", $line, FILE_APPEND);
    }
}

############# function test #############
/*
$testWord = "test";

$retval = accessDB("SEARCH", $testWord);
echo $retval."<br />";
$retval = accessDB("NEW", $testWord);
echo $retval."<br />";
$retval = accessDB("SEARCH", $testWord);
echo $retval."<br />";
$retval = accessDB("ADD", $testWord, 10);
echo $retval."<br />";
$retval = accessDB("SEARCH", $testWord);
echo $retval."<br />";
*/
#error log test
/*
try {
    $sql = new PDO();
    search("table" , $sql, $testWord);
    insert("table" , $sql, $testWord);
    update("table" , $sql, $testWord , 10);

    $sql = null:
}
catch(Exception $e) {
    echo $e->getMessage()."<br />";
    die();
}
*/
?>