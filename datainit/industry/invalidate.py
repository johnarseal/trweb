# -*- coding: UTF-8 -*-

from dbsettings import *
import MySQLdb

# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS)
cur = conn.cursor()
cur.execute("use trweb")
sql = "SELECT ric,ts FROM tr_report_annual"
cur.execute(sql)
pairArr = cur.fetchall()
cnt = 0
for row in pairArr:
    ric = row[0]
    ts = row[1]
    cnt += 1
    sql = "UPDATE tr_report_annual SET netinc_after_tax=NULL,sga_exp_tot=NULL WHERE ric='" + ric + "' AND ts='" + str(ts) + "'" 
    cur.execute(sql)
    conn.commit()
    if cnt % 1000 == 0:
        print "update " + str(cnt) + " rows"
    
    