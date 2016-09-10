# -*- coding: UTF-8 -*-
import MySQLdb,time,os,xlrd,csv,math
from dbsettings import *

# the function to handle excel
def openSH(fName,shName):
    bk = xlrd.open_workbook(fName)
    try:
        sh = bk.sheet_by_name(shName)
        return sh
    except:
        print "no sheet in " + fName + " named " + shName
        return None

print "Start to iterate through excels"
t1 = time.clock()
# the error log
errLog = open("err.log", "w")
outOfRangeLog = open("outofrange.log", "w")
noMatchLog = open("nomatch.log","w")
# the code starts to run from here   
# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS,db=DB_NAME)
cur = conn.cursor()

yearRepDict = {}
totNum = 0
ricRepeat = 0
ricRepDict = {}
maxVal = 1e24
qFolder = os.listdir(rootDir)

preSql = "INSERT INTO " + str(TB_NAME) + " (ric,ts"
for i in range(1,29):
    # no net income after tax
    if i == 4:
        continue
    preSql += "," + colDict[i]
preSql += ") VALUES('"

for folder in qFolder:
    curDir = os.path.join(rootDir,str(folder))
    docArr = os.listdir(curDir)
    for doc in docArr:
        suf = os.path.splitext(doc)[1]
        if suf.lower() != ".csv":
            continue
        filePath = os.path.join(curDir,doc)
        with open(filePath, 'rb') as csvfile:
            uKeyRec = {}
            fq2ts = {}
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            cnt = 0
            totNum += 1
            sqlDict = {}
            tsDict = {}
            # first build fq2ts
            for rowArr in spamreader:
                cnt += 1
                # the first row
                if cnt == 1:
                    continue
                if rowArr[1] == "":
                    continue
                fq = rowArr[2]
                try:
                    ts = time.strftime("%Y-%m-%d",time.strptime(rowArr[1].split(" ")[0],"%m/%d/%Y"))
                except:
                    print filePath
                    print rowArr[1]
                # assume that the first ts is correct
                if fq in fq2ts:
                    continue
                if ts in tsDict:
                    continue
                tsDict[ts] = 1
                
                fq2ts[fq] = ts

            csvfile.seek(0)
            cnt = 0
            # build first 26 variable
            for rowArr in spamreader:            
                cnt += 1
                # the first row
                if cnt == 1:
                    ric = rowArr[0]
                    continue
                if rowArr[1] == "":
                    continue                    
                ts = time.strftime("%Y-%m-%d",time.strptime(rowArr[1].split(" ")[0],"%m/%d/%Y"))
                sql = preSql
                sql += str(ric) + "','" + str(ts) + "'"
                valid = 0
                for i in range(27):
                    # no net income after tax
                    if i == 3:
                        continue
                    val = cell2val(rowArr[i+3],outOfRangeLog)
                    if val != "NULL":
                        valid = 1
                    sql += "," + str(val)
                
                sqlDict[ts] = {"sql":sql,"valid":valid,"has":0}
                    
            csvfile.seek(0)
            cnt = 0
            # build the 27th variable
            for rowArr in spamreader:
                cnt += 1
                # the first row
                if cnt == 1:
                    continue
                fq = rowArr[30]
                if fq not in fq2ts:
                    continue
                ts = fq2ts[fq]
                if ts not in sqlDict:
                    continue
                val = cell2val(rowArr[31],outOfRangeLog)
                if val == "NULL" and sqlDict[ts]["valid"] == 0:
                    continue
                sqlDict[ts]["sql"] += "," + str(val) + ")"
                sqlDict[ts]["has"] = 1
            
            for ts in sqlDict:
                if sqlDict[ts]["has"] == 1:
                    sql = sqlDict[ts]["sql"]
                else:
                    if sqlDict[ts]["valid"] == 0:
                        continue
                    else:
                        sql = sqlDict[ts]["sql"] + ",NULL)"
                try:
                    cur.execute(sql)
                    conn.commit()
                except Exception as e:
                    errLog.write(sql + "\n" + str(e) + "\n")
                    
        if totNum % 1000 == 0:
            print "Time:" + str(time.clock()) + ", Finish handling " + str(totNum) + ", ric repeat:" + str(ricRepeat)
                
                
                
        
        
        
        
        
        
        