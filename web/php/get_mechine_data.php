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
$machine=$_POST["machine"];
if($machine=="Machine2"){
    $sql_str="SELECT *  FROM [dbo].[web_KB_No_of_inspect] where Machine='".$machine."' and start_time<=GETDATE() and end_time>=GETDATE()";
}
elseif($machine=="Machine1"){
    $sql_str="SELECT Top 1 * FROM [dbo].[web_Machine1_log_text] order by NO desc";
}

$dbh = new PDO ("dblib:host=$hostname:$port;dbname=$dbname","$username","$pw");
$stmt=$dbh->query($sql_str);
$row=$stmt->fetch(PDO::FETCH_ASSOC);
echo json_encode($row,JSON_UNESCAPED_UNICODE);




?>