<?php
	require_once("dbsettings.php");
	require_once("datascheme.php");
	$ric = $_GET['ric'];
	$sql = "SELECT * FROM ".$RP_TABLE." WHERE ric = '".$ric."'";
	$result = mysqli_query($con,$sql);
	$colDict = Array();
	while($row = mysqli_fetch_assoc($result)){		
		$ts = (string)(strtotime($row['ts']) * 1000);
		foreach($row as $k => $v){
			if($k == 'pk' || $k == 'ric' || $k == 'ts'){
				continue;
			}
			if (array_key_exists($k,$colDict)){
				$colDict[$k][$ts] = $v;
			}
			else{
				$colDict[$k] = Array();
			}
		}
	}
	
	$inc_state = Array();
	$inc_state["Revenue Growth"] = calGrowth($colDict["tot_rev"]);
	
	
	$retData = Array("Income Statement"=>$inc_state,"Balance Sheet"=>Array(),"Cash Flow Statement"=>Array());
	echo json_encode($retData);
	