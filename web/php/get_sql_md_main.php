<?php

header('Content-Type: application/x-www-form-urlencoded; charset=UTF-8');
// 主機位址
$hostname = '127.0.0.1';
// PORT
$port = '1433';
// 資料庫名稱
$dbname = 'Database';
// 帳號
$username = 'User';
// 密碼
$pw = 'Password';

$kb_main_no=$_POST["kb_main_no"];

$sql_str="SELECT *  FROM [dbo].[kb_main] where no='".$kb_main_no."' order by no asc";

$dbConn = new PDO ("dblib:host=$hostname:$port;dbname=$dbname","$user","$pw");

$stmt=$dbConn->prepare($sql_str);
$stmt->execute();
$rows=$stmt->fetchAll(PDO::FETCH_ASSOC);
if ($rows==[]){
    echo null;
}
else{
foreach($rows as $row)
{
    $array[]=$row;
}
echo json_encode($array,JSON_UNESCAPED_UNICODE);;
}



?>