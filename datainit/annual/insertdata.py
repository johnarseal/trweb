# -*- coding: UTF-8 -*-
import MySQLdb,time,os,xlrd
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

# the error log
errLog = open("err.log", "w")

# the code starts to run from here   
# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS,db=DB_NAME)
cur = conn.cursor()

yearRepDict = {}
totalRow = 0
totalNull = 0
sucNum = 0
errNum = 0
ricRepeat = 0
for folder in annualFolder:
    curDir = os.path.join(rootDir,str(folder))
    docArr = os.listdir(curDir)
    for doc in docArr:
        ricRepDict = {}
        filePath = os.path.join(curDir,doc)
        curSH = openSH(filePath,"Sheet1")
        numRow = curSH.nrows
        year = str(int(curSH.cell_value(0,0)))
        
        if year in yearRepDict:
            print "Year " + str(year) + " is found repeated"
            continue
        yearRepDict[year] = 1
        ts = year[:4] + "-" + year[4:6] + "-" + year[6:8]
         
        for i in range(1,numRow):
            ric = str(curSH.cell_value(i,0))
            if ric in ricRepDict:
                ricRepeat += 1
                #print "Ric " + ric + " in " + filePath + " is found repeated"
                continue
            ricRepDict[ric] = 1
    
            # build the sql query
            nullCnt = 0
            sql = "INSERT INTO " + TB_NAME + " (ric, ts"
            for k in colDict:
                sql += ", " + colDict[k]
            sql += ") VALUES('" + ric + "', '" + ts + "'"
            for j in range(1,numCol + 1):
                val = str(curSH.cell_value(i,j))             
                if val == "NULL":
                    sql += ", NULL"
                    nullCnt += 1
                else:
                    try:
                        tmp = float(val)
                        sql += ", '" + val + "'"
                    except:
                        nullCnt += 1
                        sql += ", NULL"                   
            sql += ")"
            
            totalRow += 1
            if nullCnt == numCol:
                totalNull += 1
                continue
            
            try:
                cur.execute(sql)
                conn.commit()
                sucNum += 1
            except Exception as e:
                errLog.write(str(e) + "\n" + sql + "\n")
                errNum += 1
            
        print "Finish handling file " + doc + ", total rows:" + str(totalRow) \
        + ", null:" + str(totalNull) + ", success:" + str(sucNum) + ", error:" \
        + str(errNum) + ", ric repeat:" + str(ricRepeat)
                
                
                
        
        
        
        
        
        
        