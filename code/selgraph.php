<html>
<head>
    <link href="lib/bootstrap-3.3.5-dist/css/bootstrap.min.css" rel="stylesheet" />
    <script src="js/jquery-2.2.3.min.js"></script>
    <script src="lib/bootstrap-3.3.5-dist/js/bootstrap.min.js"></script>
</head>
<body>
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
	