<html>
<head>
<script src="js/jquery-2.2.3.min.js"></script>
  <style type="text/css">
table,th,tr,td
{
border-collapse:collapse;font-family:"Trebuchet MS";
} 
caption {font-size:30px;}
#result td, #result th, #result tr,#result 
  {
  font-size:14px;
  border:1px solid #98bf21;
  padding:1px 3px 1px 3px;
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
<caption id="resCap">Result </caption>
<tr><th>NO.</th><th>Name</th><th>Ric</th><th>Sedol</th><th>Cusip</th><th>ticker</th><th>Equity Type</th><th>Country of exchange</th><th>Exchange</th><th>GICS Industry</th><th>Status</th></tr>

<?php
	require_once("dbsettings.php");
	$showCols = Array("name","ric","sedol","cusip","company_ticker","equity","country","exchange","industry","status");
	$status = $_GET["status"];	
	
	$condKeys = Array("country","exchange","equity");
	$condNum = count($_GET[$condKeys[0]]);
	$rowCnt = 0;
	for($i = 0; $i < $condNum; $i++){
		$sql = "SELECT ";
		foreach($showCols as $col){
			$sql .= "`{$col}`,";
		}
		$sql = substr($sql, 0, -1);
		$sql .= " FROM {$masterID_TB} WHERE ";
		$hasCond = 0;
		foreach($condKeys as $key){
			if($_GET[$key][$i] != "All"){
				$sql .= "{$key} = '{$_GET[$key][$i]}' AND ";
				$hasCond = 1;
			}
		}
		if($hasCond){
			if($status == "All"){
				$sql = substr($sql, 0, -4);
			}
			else{
				$sql .= "status = '{$status}'";
			}
		}
		else{
			if($status == "All"){
				$sql = substr($sql, 0, -6);
			}
			else{
				$sql .= "status = '{$status}'";
			}
		}
		$result = mysqli_query($con,$sql);
		if($result){
			while($row = mysqli_fetch_assoc($result)){
				$rowCnt++;
				echo "<tr><td>{$rowCnt}</td>";
				foreach($showCols as $col){
					if($col == 'ric'){
						echo "<td><a href='selgraph.php?ric={$row[$col]}'>{$row[$col]}</a></td>";
					}
					else{
						echo "<td>{$row[$col]}</td>";
					}
					
				}
				echo "</tr>";
			}
		}
	}
?>
</table>
<a href="search.html">Back</a>
</center>
<?php
	echo "<script>$('#resCap').append('{$rowCnt}')</script>";
?>
</body>
</html>