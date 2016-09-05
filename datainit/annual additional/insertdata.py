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

yearRepDict = {}
totNum = 0
ricRepeat = 0
ricRepDict = {}
maxVal = 1e24
aFolder = os.listdir(rootDir)
newNum = 0

preSql = "UPDATE tr_report_annual SET "
nullSql = "INSERT INTO tr_report_annual (ric,ts) VALUES ('"
for folder in aFolder:
    curDir = os.path.join(rootDir,str(folder))
    docArr = os.listdir(curDir)
    for doc in docArr:
        suf = os.path.splitext(doc)[1]
        if suf.lower() != ".csv":
            continue
        filePath = os.path.join(curDir,doc)
        with open(filePath, 'rb') as csvfile:
            totNum += 1
            cnt = 0
            fy2date = {}
            date2fy = {}
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # we need to build a double map first
            for rowArr in spamreader:
                cnt += 1
                # the first row
                if cnt == 1:
                    ric = rowArr[0]
                    continue
                if rowArr[2] == "":
                    continue
                fy = str(rowArr[1][2:])
                ts = time.strftime("%Y-%m-%d",time.strptime(rowArr[2].split(" ")[0],"%m/%d/%Y"))
                fy2date[fy] = ts
                date2fy[ts] = fy
            
            # need to move back to the top of the file
            csvfile.seek(0)
            # the valdict to store the sql
            valDict = {}
            for rowArr in spamreader:
                cnt += 1
                # the first row
                if cnt == 1:
                    continue
                for colInd in range(2,11,2):
                    try:
                        ts = time.strftime("%Y-%m-%d",time.strptime(rowArr[colInd].split(" ")[0],"%m/%d/%Y"))
                    except Exception as e:
                        errLog.write(ric+" ts err: " + rowArr[colInd]) 
                    # every entry must have a fiscal year, else we can't define its fiscal year
                    if ts not in date2fy:
                        continue
                    fy = date2fy[ts]
                    if fy not in valDict:
                        valDict[fy] = {}
                    
                    try:
                        val = round(float(rowArr[colInd+1]),6)
                        # filter out invalid data
                        # nan
                        if math.isnan(val):
                            val = "NULL"
                            # out of range
                        elif abs(val) > maxVal:
                            outOfRangeLog.write(sql + "\n" + str(val) + "\n")
                            break
                                    
                    except Exception as e:
                        val = "NULL"  

                    valDict[fy][colInd] = val
            
            for fy in valDict:
                sqlDict = valDict[fy]
                sql = preSql
                valid = 0
                for colInd in range(2,11,2):
                    sql += colDict[colInd] + "="
                    if colInd not in sqlDict:
                        sql += "NULL,"
                    else:
                        if sqlDict[colInd] != "NULL":
                            valid = 1
                        sql += str(sqlDict[colInd]) + ","
                if valid:
                    sql += "fy=" + str(fy)
                    sql += " WHERE ric='" + ric + "' AND ts='" + str(fy2date[fy]) + "'"
                    querySql = "SELECT ric FROM tr_report_annual WHERE ric='" + ric + "' AND ts='" + fy2date[fy] + "'"
                    num = cur.execute(querySql)
                    # if not exist, insert first
                    if num == 0:
                        newNum += 1
                        insSql = nullSql + ric + "','" + str(fy2date[fy]) + "')"
                        try:
                            cur.execute(insSql)
                            conn.commit()
                        except Exception as e:
                            errLog.write(insSql+"\n"+str(e)+"\n")                        
                    
                    # update it
                    try:
                        cur.execute(sql)
                        conn.commit()
                    except Exception as e:
                        errLog.write(sql+"\n"+str(e)+"\n")
                            
        if totNum % 1000 == 0:
            print "Time:" + str(time.clock()) + ", Finish handling " + str(totNum) + ", newNum:" + str(newNum)          
        
        
        
        
        
        
        