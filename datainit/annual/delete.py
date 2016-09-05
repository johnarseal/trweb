# -*- coding: UTF-8 -*-
import MySQLdb,time,os,xlrd,csv,math
from dbsettings import *

# the code starts to run from here   
# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS,db=DB_NAME)
cur = conn.cursor()

sql = "SELECT ric FROM tr_master_id"
cur.execute(sql)
ricDict = {}
raw = cur.fetchall()
for row in raw:
    ric = row[0]
    ricDict[ric] = 1

print "fetching from annual report"

sql = "SELECT DISTINCT(ric) FROM tr_report_annual"
cur.execute(sql)
raw = cur.fetchall()
noIn = 0
for row in raw:
    ric = row[0]
    if ric not in ricDict:
        delSql = "DELETE FROM tr_report_annual WHERE ric = '" + str(ric) + "'"
        cur.execute(delSql)
        conn.commit()



