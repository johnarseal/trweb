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
# the code starts to run from here   
# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS,db=DB_NAME)
cur = conn.cursor()

preSql = "INSERT INTO tr_report_semi (ric,ts,fy"
for col in colArr:
    preSql += "," + col
preSql += ") VALUES("
colNum = len(colArr)

nullSql = preSql
for i in range(colNum-2):
    nullSql += "NULL,"
    
yearRepDict = {}
totNum = 0
ricRepeat = 0
ricRepDict = {}

semiFolder = os.listdir(rootDir)
for folder in semiFolder:
    curDir = os.path.join(rootDir,str(folder))
    docArr = os.listdir(curDir)
    for doc in docArr:
        suf = os.path.splitext(doc)[1]
        if suf.lower() != ".csv":
            continue
        filePath = os.path.join(curDir,doc)
        with open(filePath, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            cnt = 0
            fy2date = {}
            date2fy = {}
            totNum += 1
            sqlDict = {}
            for rowArr in spamreader:
                cnt += 1
                # the first row
                if cnt == 1:
                    ric = rowArr[0]
                    continue
                else:
                    # for one normal row
                    if rowArr[1] == "":
                        continue
                    try:
                        ts = time.strftime("%Y-%m-%d",time.strptime(rowArr[1].split(" ")[0],"%m/%d/%Y"))
                    except Exception as e:
                        print rowArr[1]
                        print filePath
                        exit(0)
                    fy = str(rowArr[2][2:])
                    if ts != "" and fy != "":
                        date2fy[ts] = fy
                        fy2date[fy] = ts
                    else:
                        continue
                    
                    sql = preSql + "'" + ric + "','" + ts + "','" + str(fy) + "'"
                    valid = 0
                    for colInd in range(0,colNum-2):
                        val = cell2val(rowArr[colInd+3],outOfRangeLog)
                        sql += "," + str(val)
                        if val != "NULL":
                            valid = 1
                    
                    sqlDict[fy] = {"sql":sql,"valid":valid,"comp":2}
                            
            csvfile.seek(0)
            for rowArr in spamreader:
                cnt += 1                
                # the first row
                if cnt == 1:
                    continue
                val = cell2val(rowArr[31],outOfRangeLog)
                if val == "NULL":
                    continue
                fy = str(rowArr[30][2:])
                if fy in fy2date:
                    if fy not in sqlDict:
                        sqlDict[fy] = {}
                        sqlDict[fy]["sql"] = nullSql + str(val)
                    else:
                        sqlDict[fy]["sql"] += "," + str(val)
                    sqlDict[fy]["comp"] = 1
                    sqlDict[fy]["valid"] = 1
                    
            csvfile.seek(0)
            for rowArr in spamreader:
                cnt += 1                
                # the first row
                if cnt == 1:
                    continue
                val = cell2val(rowArr[36],outOfRangeLog)
                if val == "NULL":
                    continue
                ts = time.strftime("%Y-%m-%d",time.strptime(rowArr[35].split(" ")[0],"%m/%d/%Y"))
                if ts in date2fy:
                    fy = date2fy[ts]
                    if fy not in sqlDict:
                        sqlDict[fy] = {}
                        sqlDict[fy]["sql"] = nullSql + "NULL," + str(val) + ")"
                    else:
                        if sqlDict[fy]["comp"] == 2:
                            sqlDict[fy]["sql"] += ",NULL," + str(val) + ")"
                        elif sqlDict[fy]["comp"] == 1:
                            sqlDict[fy]["sql"] += "," + str(val) + ")"
                    sqlDict[fy]["comp"] = 0
                    sqlDict[fy]["valid"] = 1

            for fy in sqlDict:
                if sqlDict[fy]["valid"]:
                    if sqlDict[fy]["comp"] == 0:
                        sql = sqlDict[fy]["sql"]
                    elif sqlDict[fy]["comp"] == 1:
                        sql = sqlDict[fy]["sql"] + ",NULL)"
                    else:
                        sql = sqlDict[fy]["sql"] + ",NULL,NULL)"
                
                    try:
                        cur.execute(sql)
                        conn.commit()
                    except Exception as e:
                        errLog.write(str(e) + "\n" + sql + "\n")
            
        if totNum % 1000 == 0:
            print "Time:" + str(time.clock()) + ", Finish handling " + str(totNum)
                
                
                
        
        
        
        
        
        
        