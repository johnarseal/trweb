<?php
	
	$con = mysqli_connect("127.0.0.1", "root");
	if (!$con)
	{
		die('Could not connect: ' . mysqli_error());
	}
	mysqli_select_db($con,"trweb");
	$RP_TABLE_AN = "tr_report_annual";
	$RP_TABLE_QU = "tr_report_quarter";
	$RP_TABLE_SA = "tr_report_semi";
	$masterID_TB = "tr_master_id";
	$exchangeINFO_TB = "tr_exchange_info";