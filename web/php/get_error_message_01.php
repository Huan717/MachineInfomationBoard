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

$sql_str="SELECT top 3 [error_time],[error_text] FROM [dbo].[web_Company_log_text] where load_start='".$load_start."'  and  error_text!=''  order by NO desc ";

$dbh = new PDO ("dblib:host=$hostname:$port;dbname=$dbname","$username","$pw");
$stmt=$dbh->query($sql_str);
$rows=$stmt->fetchAll(PDO::FETCH_ASSOC);
if($rows==[]){
  echo 'false';
}else
{
  foreach($rows as $row)
  {
    $array[]=$row;
  }
  echo json_encode($array,JSON_UNESCAPED_UNICODE);;
}


?>