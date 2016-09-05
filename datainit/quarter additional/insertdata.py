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
qFolder = os.listdir(rootDir)

preSql = "UPDATE tr_report_quarter SET "

fullColNum = len(fullColDict)
oldColNum = fullColNum - 3
nullSql = "INSERT INTO tr_report_quarter (ric,ts"
for i in range(0,fullColNum):
    nullSql += "," + fullColDict[i]
nullSql += ") VALUES('"

newNum = 0

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
            fqDict = {}
            extrafqDict = {}
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            cnt = 0
            numCol = 0
            totNum += 1
            for rowArr in spamreader:
                cnt += 1
                # the first row
                if cnt == 1:
                    ric = rowArr[0]
                    if ric in ricRepDict:
                        ricRepeat += 1
                        # this ric has been handled
                        break
                    ricRepDict[ric] = 1  
                    numCol = len(rowArr)
                    continue
                if cnt == 2:
                    continue
                else:
                    uKey = str(ric) + "-" + str(rowArr[3].split(" ")[0])
                    if uKey not in uKeyRec:
                        uKeyRec[uKey] = 1
                        # for one common row
                        valDict = {}
                        if rowArr[3] == "":
                            continue
                        try:
                            tmpTS = time.strftime("%Y-%m-%d",time.strptime(rowArr[3].split(" ")[0],"%m/%d/%Y"))
                        except Exception as e:
                            print str(e)
                            print rowArr[3]
                            print filePath
                            exit()

                        valid = 0
                        sql = preSql
                        for i in range(0,3):
                            try:
                                val = round(float(rowArr[i+4]),6)
                                # filter out invalid data
                                # nan
                                if math.isnan(val):
                                    val = "NULL"
                                # out of range
                                elif abs(val) > maxVal:
                                    outOfRangeLog.write(sql + "\n" + str(val) + "\n")
                                    valid = 0
                                    break
                                    
                                        
                            except Exception as e:
                                val = "NULL"  
                                
                            if val == "NULL":
                                sql += colDict[i] + "=NULL,"
                            else:
                                sql += colDict[i] + "=" + str(val) + ","
                                valid = 1
                            valDict[i] = val
                            
                        if valid:
                            qSql = "SELECT ric FROM tr_report_quarter WHERE ric = '" + ric + "' AND ts = '" + tmpTS + "'"
                            num = cur.execute(qSql)
                            if num == 0:
                                newSql = nullSql + str(ric) + "', '" + tmpTS + "'"
                                for i in range(0,oldColNum):
                                    newSql += ",NULL"
                                for i in range(0,3):
                                    newSql += "," + str(valDict[i])
                                newSql += ")"
                                
                                try:
                                    cur.execute(newSql)
                                    conn.commit()
                                    newNum += 1
                                except Exception as e:
                                    errLog.write(str(e) + "\n" + newSql + "\n")
                            
        if totNum % 1000 == 0:
            print "Time:" + str(time.clock()) + ", Finish handling " + str(totNum) + ", newNum:" + str(newNum)

        
        
        
        
        
        