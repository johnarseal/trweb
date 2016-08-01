# -*- coding: UTF-8 -*-
import MySQLdb,csv,time,os
from dbsettings import *

# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS,db=DB_NAME)
cur = conn.cursor()

# fetch from database
# for insert record
lastRecNum = cur.execute("SELECT * FROM " + REC_TBNAME)
rawArr = cur.fetchall()
recArr = [row[0] for row in rawArr]
recDict = {rec:1 for rec in recArr}
# for ric in database
dataRic = {}
for ind in TB_NAME:
    sql = "SELECT DISTINCT(ric) FROM " + TB_NAME[ind]
    print "Collecting rics from table " + TB_NAME[ind]
    cur.execute(sql)
    raw = cur.fetchall()
    ricArr = [x[0] for x in raw]
    for ric in ricArr:
        if ric not in dataRic:
            dataRic[ric] = 1
            
# 2.In insert_record but not in data table
for ric in recDict:
    if ric not in dataRic:
        print(ric + " recorded but not in data table")
        
# 3.In data table but not in insert_record
for ric in dataRic:
    if ric not in recDict:
        print(ric + " in data table but not recorded")
        
print("On the fly check finish!")       
        