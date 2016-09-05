# -*- coding: UTF-8 -*-
import MySQLdb,time,os,xlrd,csv,math
from dbsettings import *

# the code starts to run from here   
# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS,db=DB_NAME)
cur = conn.cursor()
querySql = "SELECT ric,ts FROM tr_report_annual WHERE fy IS NULL"
oldNum = cur.execute(querySql)
print "Initially, " + str(oldNum) + " don't have fy"
raw = cur.fetchall()
lackDict = {}
for row in raw:
    lackDict[row[0] + "-" + str(row[1])] = 1

upNum = 0
totNum = 0
errLog = open("err.log","w")
aFolder = os.listdir(rootDir)
for folder in aFolder:
    curDir = os.path.join(rootDir,str(folder))
    docArr = os.listdir(curDir)
    for doc in docArr:
        totNum += 1
        suf = os.path.splitext(doc)[1]
        if suf.lower() != ".csv":
            continue
        filePath = os.path.join(curDir,doc)
        with open(filePath, 'rb') as csvfile:   
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            cnt = 0
            for rowArr in spamreader:
                cnt += 1
                if cnt == 1:
                    ric = rowArr[0]
                    continue
                if rowArr[2] == "":
                    continue
                try:
                    ts = time.strftime("%Y-%m-%d",time.strptime(rowArr[2].split(" ")[0],"%m/%d/%Y"))
                except Exception as e:
                    print rowArr[2]
                    print filePath
                    exit()
                uKey = ric + "-" + ts
                if rowArr[1] != "" and uKey in lackDict:
                    fy = rowArr[1][2:]
                    sql = "UPDATE tr_report_annual SET fy = " + str(fy) + " WHERE ts='" + ts + "' AND ric='" + str(ric) + "'"
                    try:
                        cur.execute(sql)
                        conn.commit()
                        upNum += 1
                    except Excetion as e:
                        errLog.write(sql+"\n" + str(e) + "\n")


        if totNum % 1000 == 0:
            print "finish handle " + str(totNum) + " files, update " + str(upNum) + " records"
        
            
            
            