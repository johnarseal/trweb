# -*- coding: UTF-8 -*-

import MySQLdb,csv,time,os
from dbsettings import *

# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS,db=DB_NAME)
cur = conn.cursor()
rangeErrLog = open("rangeerr.log", "a+")

totalLine = 0
with open("outofrange.log","r") as sqlFile:
    for line in sqlFile:
        totalLine += 1

print("total sql: " + str(totalLine))

totalNum = 0
succNum = 0
errNum = 0
repeatDict = {}
with open("outofrange.log","r") as sqlFile:
    for sql in sqlFile:
        totalNum += 1
        if totalNum % 2000 == 0:
            print("Total:" + str(totalLine) + ", handled " + str(totalNum) + " sql, success:" + str(succNum) + ", err:" + str(errNum))
        if sql in repeatDict:
            errNum += 1
            continue
        repeatDict[sql] = 1
        try:
            cur.execute(sql)
            conn.commit()
            succNum += 1
        except Exception as e:
            errNum += 1
            