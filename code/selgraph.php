<html>
<head>
    <link href="lib/bootstrap-3.3.5-dist/css/bootstrap.min.css" rel="stylesheet" />
    <script src="js/jquery-2.2.3.min.js"></script>
    <script src="lib/bootstrap-3.3.5-dist/js/bootstrap.min.js"></script>
<style type="text/css">
table.gridtable {
	font-family: verdana,arial,sans-serif;
	font-size:11px;
	color:#333333;
	border-width: 1px;
	border-color: #666666;
	border-collapse: collapse;
}
table.gridtable th {
	border-width: 1px;
	padding: 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #dedede;
}
table.gridtable td {
	border-width: 1px;
	padding: 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #ffffff;
}
</style>

</head>
<body>
	<div style="margin:20px auto;width:1000px">
	<table class="table table-bordered"><tr>
	<?php 
		require_once("dbsettings.php");
		$firstCol = 10;
		$ric = $_GET["ric"];
		$sql = "SELECT * FROM {$masterID_TB} WHERE ric = '{$ric}'";
		$result = mysqli_query($con,$sql);
		$rawRow = mysqli_fetch_assoc($result);
		
		$prtRow = array_chunk($rawRow,$firstCol);
		foreach($prtRow as $ind => $valRow){
			$cntCol = $firstCol;
			if($ind == 0){
				$cntCol--;
			}
			while($cntCol-- && gettype(next($rawRow)) != null){
				echo "<th>".key($rawRow)."</th>";
			}
			echo "</tr><tr>";
			$firstFlag = 0;
			foreach($valRow as $val){
				if($ind == 0 && $firstFlag == 0){
					$firstFlag += 1;
					continue;
				}
				echo "<td>{$val}</td>";
			}
			echo "</tr>";
		}
	?>
	</tr></table>
	</div>
	<div style="margin:50px auto;width:200px">
		<a target="_blank" class="btn btn-primary btn-lg" href="graphannual.html?ric=<?php echo $_GET["ric"]?>" role="button">Annual Report</a>
		<br>
		<br>
		<a target="_blank" class="btn btn-success btn-lg" href="graphquarter.html?ric=<?php echo $_GET["ric"]?>" role="button">Quarter Report</a>
		<br>
		<br>
		<a class="btn btn-info btn-lg" href="#" role="button">Daily Price</a>
	</div>
</body>
</html>
	