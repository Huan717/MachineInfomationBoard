<?php

header('Content-Type: application/x-www-form-urlencoded; charset=UTF-8');
// 主機位址
$hostname = '127.0.0.1';
// PORT
$port = '1433';
// 資料庫名稱
$dbname = 'Database';
// 帳號
$username = 'user';
// 密碼
$pw = 'passwd';
$lot=$_POST["lot"];
//$lot='211106701';
$sql_str="select TOP 1
Database.dbo.Customer.[Name]
From Database.dbo.Customer,dbo.Obody,dbo.Ohead 
Where 
Database.dbo.[Obody].[LotNo]='".$lot."' and 
Database.dbo.Obody.Ohead_No=Database.dbo.Ohead.Ohead_No AND 
Database.dbo.Ohead.Cus_No=Database.dbo.Customer.Cus_No ";

//echo $sql_str;
//$dbConn = new PDO("sqlsrv:server=".$hostname.",".$port.";Database=".$dbname,$username,$pw);
$dbConn = new PDO ("dblib:host=$hostname:$port;dbname=$dbname","$username","$pw");
$stmt=$dbConn->query($sql_str);

$row_customer=$stmt->fetch(PDO::FETCH_ASSOC);


$dbConn=null;
$sql_str="select Company.dbo.COPTD.TD006 From Company.dbo.COPTD Where Company.dbo.COPTD.TD212='".$lot."'";
//$dbConn = new PDO("sqlsrv:server=".$hostname.",".$port.";Database=".$dbname,$username,$pw);
$dbConn = new PDO ("dblib:host=$hostname:$port;dbname=$dbname","$username","$pw");
$stmt=$dbConn->query($sql_str);
$row_size=$stmt->fetch(PDO::FETCH_ASSOC);

if($row_customer==[]){
    echo 'false';
}else
{
    $result=array_merge($row_customer,$row_size);
    echo json_encode($result,JSON_UNESCAPED_UNICODE);
}



?>