<?php
	function calGrowth($raw){
		$retData = array();
			$last = current($raw);
			$cnt = 0;
			foreach($raw as $k=>$v){
				$cnt++;
				if($cnt == 1){
					continue;
				}
				array_push($retData,array($k,($v - $last) / $last));
				$last = $v;
			}
		return $retData;
	}