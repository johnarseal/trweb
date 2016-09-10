# -*- coding: UTF-8 -*-
import MySQLdb,time,os,xlrd,csv,math
from dbsettings import *

filePath = "C:/project/Lixi/raw/additional fiscal year.csv"
# the code starts to run from here   
# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS,db=DB_NAME)
cur = conn.cursor()

errLog = open("fyerr.log","w")
sqlErrLog = open("sqlerr.log","w")

with open(filePath, 'rb') as csvfile:   
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    cnt = 0
    for rowArr in spamreader:
        cnt += 1
        if cnt == 1:
            continue
            
        if cnt % 3 == 2:
            ric = rowArr[0]
            fyDict = {}
            rowLen = len(rowArr)
            for i in range(2,rowLen):
                if rowArr[i] == "":
                    continue
                try:
                    fyDict[i] = int(rowArr[i][2:])
                except Exception as e:
                    errLog.write(ric+"\n"+"error fy:" + str(i)+"\n")
                
        elif cnt % 3 == 0:
            rowLen = len(rowArr)
            ts2fy = {}
            for i in range(2,rowLen):
                if rowArr[i] == "":
                    continue
                try:
                    ts = time.strftime("%Y-%m-%d",time.strptime(rowArr[i].split(" ")[0],"%Y/%m/%d"))
                except Exception as e:
                    errLog.write(ric+"\n"+"error ts:"+int(i)+"\n")
                if i in fyDict:
                    ts2fy[ts] = fyDict[i]
        
        elif cnt % 3 == 1:
            for ts in ts2fy:
                querySql = "SELECT fy FROM tr_report_annual WHERE ric = '" + ric + "' AND ts = '" + ts + "'"
                if cur.execute(querySql) == 0:
                    continue
                raw = cur.fetchall()
                if raw[0][0] != None:
                    continue
                sql = "UPDATE tr_report_annual SET fy = " + str(ts2fy[ts]) + " WHERE ric = '" + ric + "' AND ts = '" + ts + "'"
                try:
                    cur.execute(sql)
                    conn.commit()
                except Exception as e:
                    sqlErrLog.write(str(e)+"\n"+sql+"\n")

        if cnt % 10000 == 0:
            print "finish handle " + str(cnt) + " rows"
        
            
            
            