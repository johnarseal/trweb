# -*- coding: UTF-8 -*-

from dbsettings import *
import MySQLdb

# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS)
cur = conn.cursor()

# switch to trweb
cur.execute("USE trweb")

# create table for the daily table
sql = "CREATE TABLE IF NOT EXISTS " + TB_NAME + """ ( 
    `pk` int unsigned AUTO_INCREMENT PRIMARY KEY,
    ric varchar(32) NOT NULL DEFAULT '',
    ts date NOT NULL,
    tot_rev decimal(24,8) NULL,
    sga_exp_tot decimal(24,8) NULL,
    cost_rev_tot decimal(24,8) NULL,
    netinc_after_tax decimal(24,8) NULL,
    tot_com_share_ostd decimal(24,8) NULL,
    tot_pref_share_ostd decimal(24,8) NULL,
    acc_rec_trade decimal(24,8) NULL,
    acc_pay decimal(24,8) NULL,
    tot_invent decimal(24,8) NULL,
    tot_asset_rep decimal(24,8) NULL,
    tot_cur_asset decimal(24,8) NULL,
    cash_shortterm_invest decimal(24,8) NULL,
    accrued_exp decimal(24,8) NULL,
    tot_longterm_debt decimal(24,8) NULL,
    tot_debt decimal(24,8) NULL,
    tot_equity decimal(24,8) NULL,
    cap_lease decimal(24,8) NULL,
    tot_liability decimal(24,8) NULL,
    tot_cur_liability decimal(24,8) NULL,
    tot_property decimal(24,8) NULL,
    cash_operating decimal(24,8) NULL,
    cash_finance decimal(24,8) NULL,
    cash_invest decimal(24,8) NULL,
    foreign_exch decimal(24,8) NULL,
    cash_divid_paid decimal(24,8) NULL,    
    INDEX  ind_ric(ric)  
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
cur.execute(sql)

sql = "ALTER TABLE " + TB_NAME + " ADD UNIQUE `ric_ts_unique`(`ric`, `ts`)"
cur.execute(sql)
# commit changes
conn.commit()