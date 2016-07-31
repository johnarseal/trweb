# -*- coding: UTF-8 -*-

import MySQLdb,csv,time,os,math,signal,sys
from dbsettings import *
from insertfunc import *

# the code starts to run from here   
# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS,db=DB_NAME)
cur = conn.cursor()
recordErrLog = open("recorderr.log", "a+")

"""
# making up for check 1
totalErr = 0
with open("check1.log","rb") as pathFile:
    for line in pathFile:
        path = line[:-1].decode('utf-8')
        # making up for check 1
        totalErr += insertSingleFile(path,TB_NAME,cur)
        fileName = os.path.basename(path)
        docPair = os.path.splitext(fileName)
        docRic = docPair[0]
        sql = "INSERT INTO " + REC_TBNAME + " VALUES ('" + docRic + "')"
        try:
            cur.execute(sql)
        except Exception as e:
            recordErrLog.write(str(e) + "\n" + sql + "\n")        
        conn.commit()
     
print("Finish make up for check 1, total uncaught error:" + str(totalErr))
"""


# making up for check 2
totalErr = 0
totalInsert = 0
with open("check2.log","rb") as pathFile:
    for line in pathFile:
        path = line[:-1].decode('utf-8')
        # making up for check 2
        insertNum,errNum = insertSingleFile(path,TB_NAME,cur,1)
        totalErr += errNum
        totalInsert += insertNum
        fileName = os.path.basename(path)
        docPair = os.path.splitext(fileName)
        docRic = docPair[0]
        if docRic in file2RicDict:
           docRic = file2RicDict[docRic]
            
        sql = "INSERT INTO " + REC_TBNAME + " VALUES ('" + docRic + "')"
        try:
            cur.execute(sql)
        except Exception as e:
            recordErrLog.write(str(e) + "\n" + sql + "\n")        
        conn.commit()
     
print("Finish make up for check 2, insert rows:" + str(totalInsert) + ", total uncaught error:" + str(totalErr))
