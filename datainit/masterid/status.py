# -*- coding: UTF-8 -*-

from dbsettings import *
import MySQLdb

# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS)
cur = conn.cursor()
cur.execute("use trweb")
sql = "SELECT ric FROM tr_master_id"
cur.execute(sql)
ricArr = cur.fetchall()
cnt = 0
for row in ricArr:
    ric = row[0]
    cnt += 1
    if ric.find("^") > 0:
        sql = "UPDATE tr_master_id SET status='Delisted' WHERE ric='" + ric + "'"
    else:
        sql = "UPDATE tr_master_id SET status='Live' WHERE ric='" + ric + "'"
    cur.execute(sql)
    conn.commit()
    if cnt % 10000 == 0:
        print "update " + str(cnt) + " rows"
    
    