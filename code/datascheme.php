<?php
	//direct convert
	function dirConvert($raw){
		$retData = array();
		foreach($raw as $k=>$v){
			array_push($retData,array($k,$v * 1));
		}
		return $retData;
	}



	function calGrowth($raw,$format=0){
		$retData = array();
			$last = current($raw);
			$cnt = 0;
			foreach($raw as $k=>$v){
				$cnt++;
				if($cnt == 1){
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