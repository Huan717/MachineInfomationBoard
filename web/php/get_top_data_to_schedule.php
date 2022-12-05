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

$load_start=$_POST["load_start"];

$sql_str="SELECT *  FROM [dbo].[web_Machine1_log_text] where load_start='".$load_start."' order by NO asc";
//echo $sql_str;
$dbConn = new PDO ("dblib:host=$hostname:$port;dbname=$dbname","$user","$pw");
//$dbConn = new PDO("sqlsrv:server=".$hostname.",".$port.";Database=".$dbname,$username,$pw);
$stmt=$dbConn->prepare($sql_str);
$stmt->execute();
$rows=$stmt->fetchAll(PDO::FETCH_ASSOC);
foreach($rows as $row)
{
    $array[]=$row;
}
echo json_encode($array,JSON_UNESCAPED_UNICODE);;
 


?>