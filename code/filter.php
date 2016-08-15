<?php 
  	
  function searchNextLevel($keyArr,$condArr,&$multiKey)
  {
      $curInd = count($condArr);
      $total = count($keyArr);
      $sql = "SELECT DISTINCT ".$keyArr[$curInd]." FROM `mytable` ";
      if($curInd > 0){
        $sql .= "WHERE ";
      }
      for($i = 0; $i < $curInd; $i++){
          $sql .= $keyArr[$i] ."="."'".$condArr[$i]."' AND ";
      }
      if($curInd > 0){
        $sql = substr($sql, 0, -4);
      }
      $result=mysqli_query($con,$sql);
      if($result){
        while($row = mysqli_fetch_array($result)){
          $curVal = $row[$keyArr[$curInd]];
          $multiKey[$curVal] = Array();
          if($curInd < $total-1){
            $newCond = $condArr;
            array_push($newCond,$curVal);
            searchNextLevel($keyArr,$newCond,$multiKey[$curVal]);
          }
        }
      }
  }

	// the code starts to run here
	require_once("dbsettings.php");
  
  $keyLevel = Array("market_type","country","exchange");
  $levelNum = count($keyLevel);
  $levelDict = Array();

  for($i = 0; $i < $levelNum; $i++){
    $curKey = $keyLevel[$i];
    $levelDict[$curKey] = Array();
    $sql = "SELECT DISTINCT ".$curKey." FROM {$exchangeINFO_TB}";
    $result = mysqli_query($con,$sql);
    if($result){
      while($row = mysqli_fetch_assoc($result)){   
        $curVal = $row[$curKey];
        $levelDict[$curKey][$curVal] = Array();
        if($i < $levelNum-1){
          $sql = "SELECT DISTINCT ".$keyLevel[$i+1]." FROM {$exchangeINFO_TB} WHERE ".$curKey."='".$curVal."'";
          $subResult=mysqli_query($con,$sql);
          if($subResult){
            while($subRow = mysqli_fetch_assoc($subResult)){
              array_push($levelDict[$curKey][$curVal],$subRow[$keyLevel[$i+1]]);
            }
          }           
        }
      }
    }  
  }
  
	$normFil = Array("equity","sector");
	$filData = Array();
	foreach($normFil as $col){
		$filData[$col] = Array();
		$sql = "SELECT DISTINCT {$col} FROM {$masterID_TB}";
		$result = mysqli_query($con,$sql);
		if($result){
			while($row = mysqli_fetch_assoc($result)){
				array_push($filData[$col],$row[$col]);
			}
		}
	}
	$retData = Array("levelDict"=>$levelDict,"filData"=>$filData);


	
  //searchNextLevel($keyLevel,Array(),$levelDict);
  echo json_encode($retData);
  ?>
 



