<html>
<head>
  <style type="text/css">
table,th,tr,td
{
border-collapse:collapse;font-family:"Trebuchet MS";
} 
</style>
<style>
caption {font-size:30px;}
#result td, #result th, #result tr,#result 
  {
  font-size:1em;
  border:1px solid #98bf21;
  padding:3px 7px 2px 7px;
  }
#result th 
  {
  font-size:1.1em;
  text-align:left;
  padding-top:5px;
  padding-bottom:4px;
  background-color:#A7C942;
  color:#ffffff;
  }
#result td.alt{
  color:#000000;
  background-color:#EAF2D3;
  }
</style>
</head>
<body>
<center>
<table id="result">
<caption>Result</caption>
<tr><th>Name</th><th>Ric</th><th>Type of Equity</th><th>Country of exchange</th><th>Exchange</th><th>GICS Industry</th></tr>

<?php
	$condKeys = Array("market_type","country","exchange","equity","industry");
	$condNum = count($_GET[$condKeys[0]]);
	for($i = 0; $i < $condNum; $i++){
		$sql = "SELECT * FROM mytable WHERE ";
		$hasCond = 0;
		foreach($condKeys as $key){
			if($_GET[$key][$i] != "All"){
				$sql .= "{$key} = {$_GET[$key][$i]} AND ";
				$hasCond = 1;
			}
		}
		if($hasCond){
			$sql = substr($sql, 0, -4);
		}
		else{
			$sql = substr($sql, 0, -6);
		}
		$result = mysqli_query($sql);
		if($result){
			while($row = mysqli_fetch_array($result)){
				echo "<tr><td>{$row['COL 1']}</td><td><a href='{$row['COL 2']}.html'>{$row['COL 2']}</a></td><td>{$row['equity']}</td><td>{$row['country']}</td><td>{$row['exchange']}</td><td>{$row['industry']}</td></tr>";
			}
		}
	}
?>
</table>
<a href="search.html">Back</a>

</center>
</body>
</html>