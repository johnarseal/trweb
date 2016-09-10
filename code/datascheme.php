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


	//format=1:return to html; 0:still needed to be used
	//caculate the growth of a metric
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
					$retData[$k] = ($v - $last) / abs($last);					//we are dividing by abs value
				}
				else if($format == 1){
					array_push($retData,array($k,($v - $last) / abs($last)));	//we are dividing by abs value
				}	
				$last = $v;
			}
		return $retData;
	}
	
	//caculate the growth of a metric by last year, used for quarter graph
	function calGrowthLY($raw,$format=0){
		$variance = 20*24*3600;
		$yearGap = 365*24*3600;
		if($raw==NULL){
			return NULL;
		}
		$newRaw = array();
		$retData = array();
		foreach($raw as $k=>$v){
			$ts = (int)substr($k,0,-3);
			$newRaw[$ts] = $v;
		}
		foreach($newRaw as $k=>$v){
			if($v == 0){
				continue;
			}
			$tmpArr = $newRaw;
			$curTS = $k;
			$nextTS = key($tmpArr);
			$newV = NULL;
			while($nextTS - $curTS < $yearGap + $variance){
				if(abs($nextTS - $curTS - $yearGap) < $variance){
					$newK = (string)($nextTS * 1000);
					$newV = (current($tmpArr) - $v) / abs($v);			//we are dividing by abs value
					break;
				}
				if(next($tmpArr) === false){
					//end of the array
					break;
				}
				$nextTS = key($tmpArr);
			}
			if($newV != NULL){
				if($format == 0){
					$retData[$newK] = $newV;
				}
				else if($format == 1){
					array_push($retData,array($newK,$newV));
				}					
			}
		}
		return $retData;
	}
	
	// the relationship between two metric
	//rela=0:'/' rela=1:'-' rela=2:'*' rela=3:'+' format=1:return
	function calRela($raw1,$raw2,$rela=0,$format=0,$debug=0){
		if($raw1 === NULL || $raw2 === NULL){
			return NULL;
		}
		$retData = array();
		$nv1 = current($raw1);
		$nv2 = current($raw2);
		while(1){
			//end of the array
			if($nv1 === false || $nv2 === false){
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
				else if($rela == 2){
					$val = $v1 * $v2;
				}
				else if($rela == 3){
					$val = $v1 + $v2;
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
		if($raw1===NULL || $raw2===NULL){
			return NULL;
		}
		$retData = array();
		$nv1 = current($raw1);
		$nv2 = current($raw2);		
		while(1){
			//end of the array
			if($nv1 === false || $nv2 === false){
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
	
	