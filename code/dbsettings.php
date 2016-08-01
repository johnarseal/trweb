<?php
	
	$con = mysqli_connect("127.0.0.1", "root");
	if (!$con)
	{
		die('Could not connect: ' . mysqli_error());
	}
	mysqli_select_db($con,"trweb");
	$RP_TABLE = "tr_report_annual";