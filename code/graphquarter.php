<?php
	require_once("dbsettings.php");
	require_once("datascheme.php");
	$ric = $_GET['ric'];
	$sql = "SELECT * FROM {$RP_TABLE_QU} WHERE ric = '".$ric."'";
	$result = mysqli_query($con,$sql);
	$colDict = Array();
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
	
	$normCol = Array("tot_rev","sga_exp_tot","cost_rev_tot","netinc_after_tax","tot_com_share_ostd",
				"revenue","acc_rec_trade","acc_pay","tot_invent","tot_asset_rep","tot_cur_asset",
				"cash_shortterm_invest","accrued_exp","tot_longterm_debt","tot_debt","tot_equity",
				"cap_lease","tot_cur_liability","cur_ratio","tot_property","cash_operating","cash_finance",
				"cash_invest","foreign_exch","cash_divid_paid");
	
	foreach($normCol as $col){
		if(!array_key_exists($col,$colDict)){
			$colDict[$col] = NULL;
		}
	}
	
	$inc_state = Array();
	
	$inc_state["Revenue Growth"] = calGrowth($colDict["tot_rev"],1);
	$inc_state["Revenue Growth(by last year)"] = calGrowthLY($colDict["tot_rev"],1);
	$inc_state["SG&A Growth"] = calGrowth($colDict["sga_exp_tot"],1);
	$inc_state["SG&A Growth(by last year)"] = calGrowthLY($colDict["sga_exp_tot"],1);
	$inc_state["Cost of Revenue Growth"] = calGrowth($colDict["cost_rev_tot"],1);
	$inc_state["Cost of Revenue Growth(by last year)"] = calGrowthLY($colDict["cost_rev_tot"],1);
	$inc_state["Net Income Growth"] = calGrowth($colDict["netinc_after_tax"],1);
	$inc_state["Net Income Growth(by last year)"] = calGrowthLY($colDict["netinc_after_tax"],1);
	$inc_state["Cost of Revenue/Total Revenue"] = calRela($colDict["cost_rev_tot"],$colDict["tot_rev"],0,1);
	$inc_state["SG&A/Total Revenue"] = calRela($colDict["sga_exp_tot"],$colDict["tot_rev"],0,1);
	$inc_state["Net Income/Total Revenue"] = calRela($colDict["netinc_after_tax"],$colDict["tot_rev"],0,1);
	$inc_state["Net Income/Total Revenue"] = calRela($colDict["netinc_after_tax"],$colDict["tot_rev"],0,1);
	$net_inc_oper_cash = calRela($colDict["netinc_after_tax"],$colDict["cash_operating"],1,0);
	$inc_state["(Net Income-Operating Cash Flows)/Total Assets"] = calRela($net_inc_oper_cash,$colDict["tot_asset_rep"],0,1);
	$inc_state["(Net Income-Operating Cash Flows)/Total Revenue"] = calRela($net_inc_oper_cash,$colDict["tot_rev"],0,1);
	$inc_state["(Net Income-Operating Cash Flows)/Net Income"] = calRela($net_inc_oper_cash,$colDict["netinc_after_tax"],0,1);
	$inc_state["(Net Income-Operating Cash Flows)/Total Common Shares"] = calRela($net_inc_oper_cash,$colDict["tot_com_share_ostd"],0,1);
	
	$bal_sh = Array();
	$bal_sh["Accounts Receivables/Total Revenue"] = calRela($colDict["acc_rec_trade"],$colDict["tot_rev"],0,1);
	$bal_sh["Total Inventory/Total Revenue"] = calRela($colDict["tot_invent"],$colDict["tot_rev"],0,1);
	$bal_sh["Accounts Payable/Total Revenue"] = calRela($colDict["acc_pay"],$colDict["tot_rev"],0,1);
	$bal_sh["Accrued Expenses/Total Assets"] = calRela($colDict["accrued_exp"],$colDict["tot_asset_rep"],0,1);
	$bal_sh["Accounts Receivables/Current Assets"] = calRela($colDict["acc_rec_trade"],$colDict["tot_cur_asset"],0,1);
	$bal_sh["Total Inventory/Current Assets"] = calRela($colDict["tot_invent"],$colDict["tot_cur_asset"],0,1);
	
	$acc_pay_acc_rec = calRela($colDict["acc_pay"],$colDict["acc_rec_trade"],1,0);
	$bal_sh["Accounts Payable-Accounts Receivable Growth"] = calGrowth($acc_pay_acc_rec,1);
	$bal_sh["Accounts Payable-Accounts Receivable Growth(by last year)"] = calGrowthLY($acc_pay_acc_rec,1);	
	
	
	$bal_sh["Accounts Payable-Accounts Receivable"] = calRela($colDict["acc_pay"],$colDict["acc_rec_trade"],1,1);
	
	$bal_sh["Cash and Short Term Investment/Total Assets"] = calRela($colDict["cash_shortterm_invest"],$colDict["tot_asset_rep"],0,1);
	$bal_sh["Cash and Short Term Investment/Current Assets"] = calRela($colDict["cash_shortterm_invest"],$colDict["tot_cur_asset"],0,1);
	$bal_sh["Total Long Term Debt/Total Equity"] = calRela($colDict["tot_longterm_debt"],$colDict["tot_equity"],0,1);
	$bal_sh["Total Long Term Debt/Total Assets"] = calRela($colDict["tot_longterm_debt"],$colDict["tot_asset_rep"],0,1);
	$bal_sh["Total Debt/Total Assets"] = calRela($colDict["tot_debt"],$colDict["tot_asset_rep"],0,1);
	$bal_sh["Total Debt/Total Total Equity"] = calRela($colDict["tot_debt"],$colDict["tot_equity"],0,1);
	$bal_sh["Current Portion of Long Term Debt/Total Debt"] = calRela($colDict["cap_lease"],$colDict["tot_debt"],0,1);
	$bal_sh["Current Liabilities/Current Assets"] = calRela($colDict["tot_cur_liability"],$colDict["tot_cur_asset"],0,1);
	$cur_lia_cur_assets = calRela($colDict["tot_cur_liability"],$colDict["tot_cur_asset"],1,0);
	$bal_sh["(Current Liabilities-Current Assets)/Total Assets"] = calRela($cur_lia_cur_assets,$colDict["tot_asset_rep"],0,1);
	$PPE_gro = calGrowth($colDict["tot_property"],0);	
	$bal_sh["PPE Growth/Total Assets"] = calRela($PPE_gro,$colDict["tot_asset_rep"],0,1);
	$bal_sh["Cash and Short Term Investment/Current Liabilities"] = calRela($colDict["cash_shortterm_invest"],$colDict["tot_cur_liability"],0,1);

	$cash_flow = Array();
	$cash_flow["Cash from Operating Activities Growth"] = calGrowth($colDict["cash_operating"],1);
	$cash_flow["Cash from Operating Activities Growth(by last year)"] = calGrowthLY($colDict["cash_operating"],1);
	$cash_flow["Cash from Financing Activities Growth"] = calGrowth($colDict["cash_finance"],1);
	$cash_flow["Cash from Financing Activities Growth(by last year)"] = calGrowthLY($colDict["cash_finance"],1);
	$cash_flow["Cash from Investing Activities Growth"] = calGrowth($colDict["cash_invest"],1);
	$cash_flow["Cash from Investing Activities Growth(by last year)"] = calGrowthLY($colDict["cash_invest"],1);
	$cash_flow["Foreign Exchange Effects on Cash"] = dirConvert($colDict["foreign_exch"]);
	$cash_flow["Cash Dividends Paid/Cash and Short Term Investment"] = calRela($colDict["cash_divid_paid"],$colDict["cash_shortterm_invest"],0,1);
	$cash_flow["Cash Dividends Paid Growth"] = calGrowth($colDict["cash_divid_paid"],1);
	$cash_flow["Cash Dividends Paid Growth(by last year)"] = calGrowthLY($colDict["cash_divid_paid"],1);
	
	
	/* @TODO industry
	$sql = "SELECT ric,industry,sub_industry,sector,country FROM tr_master_id WHERE ric='{$ric}'";
	$result = mysqli_query($con,$sql);
	$row = mysqli_fetch_assoc($result);
	
	$sub_industry = $row["sub_industry"];
	$sql = "SELECT * FROM tr_industry_sum WHERE type_level = 'sub_industry' AND name = '{$sub_industry}'";
	$result = mysqli_query($con,$sql);
	if($result->num_rows == 0){
		$sql = "SELECT ric FROM tr_master_id WHERE sub_industry = '{$sub_industry}'";
		$result = mysqli_query($con,$sql);
		$ricArr = Array();
		while($row = mysqli_fetch_assoc($result)){
			array_push($ricArr,$row["ric"]);
		}
		foreach($ricArr as $ric){
			$sql = "SELECT * FROM {$RP_TABLE_AN} WHERE ric = '{$ric}'
		}
	}	
	*/
	
	
	$retData = Array("Income Statement"=>$inc_state,"Balance Sheet"=>$bal_sh,"Cash Flow Statement"=>$cash_flow);
	echo json_encode($retData);
	