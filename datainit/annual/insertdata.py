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
annualFolder = os.listdir(rootDir)
for folder in annualFolder:
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
            numCol = 0
            insertRec = {}
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
                else:
                    # for one row
                    if rowArr[2] == "":
                        continue
                    tmpTS = time.strftime("%Y-%m-%d",time.strptime(rowArr[2],"%m/%d/%Y"))
                    uKey = ric + "-" + str(tmpTS)
                    if uKey in insertRec:
                        continue
                    insertRec[uKey] = 1
                    valid = 0
                    sql = "INSERT INTO " + str(TB_NAME) + " (ric,ts"
                    for i in range(3,numCol):
                        sql += "," + colDict[i-2]
                    sql += ") VALUES('" + str(ric) + "','" + str(tmpTS) + "'"
                    for i in range(3,numCol):
                        try:
                            val = round(float(rowArr[i]),6)
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
                            sql += ",NULL"
                        else:
                            sql += ",'" + str(val) + "'"
                            valid = 1

                    if valid:
                        sql += ")"
                        try:
                            cur.execute(sql)
                            conn.commit()
                        except Exception as e:
                            errLog.write(str(e) + "\n" + sql + "\n")
  
        if totNum % 1000 == 0:
            print "Time:" + str(time.clock()) + ", Finish handling " + str(totNum) + ", ric repeat:" + str(ricRepeat)
                
                
                
        
        
        
        
        
        
        