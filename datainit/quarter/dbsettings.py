# coding=utf-8
import math

# seetings for the database
RAW_HOST = 'localhost'
RAW_USER = 'root'
RAW_PASS = ''
DB_NAME = 'trweb'
REC_TBNAME = 'tr_insert_record'
TB_NAME = 'tr_report_quarter'

rootDir = u"D:/Quarter"
colDict = {
    1:"tot_rev",
    2:"sga_exp_tot",
    3:"cost_rev_tot",
    4:"netinc_after_tax",
    5:"tot_com_share_ostd",
    6:"tot_pref_share_ostd",
    7:"acc_rec_trade",
    8:"acc_pay",
    9:"tot_invent",
    10:"tot_asset_rep",
    11:"tot_cur_asset",
    12:"cash_shortterm_invest",
    13:"accrued_exp",
    14:"tot_longterm_debt",
    15:"tot_debt",
    16:"tot_equity",
    17:"cap_lease",
    18:"tot_liability",
    19:"tot_cur_liability",
    20:"tot_property",
    21:"cash_operating",
    22:"cash_finance",
    23:"cash_invest",
    24:"foreign_exch",
    25:"cash_divid_paid",
    26:"historic_pe",
    27:"bookval_pershare",
    28:"earning_pershare"
}    
numCol = len(colDict)

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

    