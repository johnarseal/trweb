# coding=utf-8
import math

# seetings for the database
RAW_HOST = 'localhost'
RAW_USER = 'root'
RAW_PASS = ''
DB_NAME = 'trweb'
REC_TBNAME = 'tr_insert_record'
TB_NAME = 'tr_report_quarter'

rootDir = u"D:/QuarterlySAaddtional"

colArr = (
    "tot_rev",
    "sga_exp_tot",
    "cost_rev_tot",
    "netinc_after_tax",
    "tot_com_share_ostd",
    "tot_pref_share_ostd",
    "acc_rec_trade",
    "acc_pay",
    "tot_invent",
    "tot_asset_rep",
    "tot_cur_asset",
    "cash_shortterm_invest",
    "accrued_exp",
    "tot_longterm_debt",
    "tot_debt",
    "tot_equity",
    "cap_lease",
    "tot_liability",
    "tot_cur_liability",
    "tot_property",
    "cash_operating",
    "cash_finance",
    "cash_invest",
    "foreign_exch",
    "cash_divid_paid",
    "historic_pe",
    "bookval_pershare",
    "earning_pershare",
    "netinc_before_extra"
)

numCol = len(colArr)

def cell2val(cellVal,outOfRangeLog):
    maxVal = 1e24
    try:
        val = round(float(cellVal),6)
        # filter out invalid data
        # nan
        if math.isnan(val):
            val = "NULL"
            # out of range
        elif abs(val) > maxVal:
            outOfRangeLog.write("outofrange err\n" + str(val) + "\n")
            val = "NULL"
    except Exception as e:
        val = "NULL"
    
    return val
    