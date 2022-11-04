<?php 
// $ip=$_SERVER["REMOTE_ADDR"]; 
// $ban=file_get_contents("ip"); //需要创建一个ip文件，里面是黑名单
// if(stripos($ban,$ip)) 
// { 
//   die("No");   
// }
//黑名单
$banned_ip = array (
"127.0.0.1"
);
if (in_array( getenv("REMOTE_ADDR"), $banned_ip ) )
{
die ("No");
}
?>