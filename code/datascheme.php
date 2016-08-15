<?php
	//direct convert
	function dirConvert($raw){
		if($raw==NULL){
			return NULL;
		}
		$retData = array();
		foreach($raw as $k=>$v){
			array_push($retData,array($k,$v * 1));
		}
		return $retData;
	}



	function calGrowth($raw,$format=0){
		if($raw==NULL){
			return NULL;
		}
		$retData = array();
			$last = current($raw);
			$cnt = 0;
			foreach($raw as $k=>$v){
				$cnt++;
				if($cnt == 1){
					continue;
				}
				if($last == 0){
					$last = $v;
					continue;
				}
				if($format == 0){
					$retData[$k] = ($v - $last) / $last;
				}
				else if($format == 1){
					array_push($retData,array($k,($v - $last) / $last));
				}
				$last = $v;
			}
		return $retData;
	}
	
	//rela=0:/ rela=1:- format=1:return
	function calRela($raw1,$raw2,$rela=0,$format=0){
		if($raw1==NULL || $raw2==NULL){
			return NULL;
		}
		$retData = array();
		$nv1 = current($raw1);
		$nv2 = current($raw2);		
		while(1){
			if($nv1 == false || $nv2 == false){
				break;
			}
			$strK1 = key($raw1);
			$strK2 = key($raw2);
			$k1 = strval($strK1);
			$k2 = strval($strK2);
			if($k1 > $k2){
				$nv2 = next($raw2);
			}
			else if($k1 < $k2){
				$nv1 = next($raw1);
			}
			else{
				$v1 = current($raw1);
				$v2 = current($raw2);
				if($rela == 0){
					if($v2 == 0){
						$nv1 = next($raw1);
						$nv2 = next($raw2);
						continue;
					}
					$val = $v1 / $v2;
				}
				else if($rela == 1){
					$val = $v1 - $v2;
				}
				
				if($format == 0){
					$retData[$strK1] = $val;
				}
				else if($format == 1){
					array_push($retData,array($k1,$val));
				}
				$nv1 = next($raw1);
				$nv2 = next($raw2);
			}
		}
		return $retData;
	}


	//rela=0:/ rela=1:- format=1:return
	function calMerge($raw1,$raw2,$rela=0,$format=0){
		if($raw1==NULL || $raw2==NULL){
			return NULL;
		}
		$retData = array();
		$nv1 = current($raw1);
		$nv2 = current($raw2);		
		while(1){
			if($nv1 == false || $nv2 == false){
				break;
			}
			$strK1 = key($raw1);
			$strK2 = key($raw2);
			$k1 = strval($strK1);
			$k2 = strval($strK2);
			if($k1 > $k2){
				$nv2 = next($raw2);
			}
			else if($k1 < $k2){
				$nv1 = next($raw1);
			}
			else{
				$v1 = current($raw1);
				$v2 = current($raw2);
				if(is_array($v1)){
					array_push($retData[$strK1],$v2);
				}
				else{
					$retData[$strK1] = Array($v1,$v2);
				}
				$nv1 = next($raw1);
				$nv2 = next($raw2);
			}
		}
		return $retData;
	}






	
	function calBatch($colDict){
		
		
		
	}
	
	function sumStat($batchDict){

		
	}
	
	function normRaw($result){
		while($row = mysqli_fetch_assoc($result)){		
			$ts = (string)(strtotime($row['ts']) * 1000);
			foreach($row as $k => $v){
				if($k == 'pk' || $k == 'ric' || $k == 'ts' || $v == null){
					continue;
				}
				if (!array_key_exists($k,$colDict)){
					$colDict[$k] = Array();
				}
				$colDict[$k][$ts] = $v;
			}
		}
	}
	
	