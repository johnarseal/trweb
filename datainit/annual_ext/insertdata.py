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

print "Start to iterate through csvs"
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
                    continue
                else:
                    # for one row
                    if rowArr[1] == "":
                        continue
                    tmpTS = time.strftime("%Y-%m-%d",time.strptime(rowArr[1],"%m/%d/%Y"))
                    uKey = ric + "-" + str(tmpTS)
                    if uKey in insertRec:
                        continue
                    insertRec[uKey] = 1
                    valid = 0
                    
                    val = {}
                    for i in range(2,4):
                        try:
                            val[i] = round(float(rowArr[i]),6)
                            if math.isnan(val[i]):
                                val[i] = "NULL"
                            # out of range
                            elif abs(val[i]) > maxVal:
                                outOfRangeLog.write(sql + "\n" + str(val[i]) + "\n")
                                valid = 0
                                break
                            else:
                                valid = 1
                        except:
                            val[i] = "NULL"
                    
                    if valid:
                        sql = "UPDATE " + str(TB_NAME) + " SET netinc_after_tax=" + str(val[2]) + ", sga_exp_tot=" + str(val[3]) + " WHERE ric = '" + ric + "' AND ts = '" + tmpTS + "'"
                        try:
                            cur.execute(sql)
                            conn.commit()
                        except Exception as e:
                            errLog.write(str(e) + "\n" + str(sql) + "\n")
  
        if totNum % 1000 == 0:
            print "Time:" + str(time.clock()) + ", Finish handling " + str(totNum) + ", ric repeat:" + str(ricRepeat)
                
                
                
        
        
        
        
        
        
        