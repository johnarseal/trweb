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
  font-size:1em;
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
<tr><th>NO.</th><th>Name</th><th>Ric</th><th>Type of Equity</th><th>Country of exchange</th><th>Exchange</th><th>GICS Industry</th><th>Status</th></tr>

<?php
	require_once("dbsettings.php");
	$showCols = Array("name","ric","equity","country","exchange","industry","status");
	
	$ric = $_GET["ric"];
	$sql = "SELECT * FROM {$masterID_TB} WHERE ric LIKE '%{$ric}%'";
	$result = mysqli_query($con,$sql);
	$rowCnt = 0;
	if($result){
		while($row = mysqli_fetch_assoc($result)){
			$rowCnt++;
			echo "<tr><td>{$rowCnt}</td>";
			foreach($showCols as $col){
				if($col == 'ric'){
					echo "<td><a href='batchgraph.html?ric={$row[$col]}'>{$row[$col]}</a></td>";
				}
				else{
					echo "<td>{$row[$col]}</td>";
				}
				
			}
			echo "</tr>";
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