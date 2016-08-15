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
ricRepLog = open("ricrepeat.log", "w")

# the code starts to run from here   
# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS,db=DB_NAME)
cur = conn.cursor()

ricRepDict = {}
totalRow = 0
sucNum = 0
errNum = 0
ricRepeat = 0

curSH = openSH(filePath,"new ID file")
numRow = curSH.nrows
numCol = curSH.ncols
for i in range(1,numRow):
    totalRow += 1
    
    ric = curSH.cell_value(i,1)
    if ric in ricRepDict:
        ricRepeat += 1
        ricRepLog.write(ric+"\r\n")
        continue
    ricRepDict[ric] = 1
    
    sql = "INSERT INTO " + TB_NAME + " ("
    for ind in col2Key:
        sql += col2Key[ind] + ", "
    sql = sql[:-2]
    sql += ") VALUES("
    
    for j in range(numCol):
        val = curSH.cell_value(i,j)
        if j == 12 or j == 13:
            if val == "Yes":
                val = 1
            elif val == "No":
                val = 0
        if val == 'NULL' or val == '' or (j == 14 and val == '--'):
            sql += "NULL, "
        else:
            sql += '"' + str(val) + '", '
    sql = sql[:-2]
    sql += ")"
    try:
        cur.execute(sql)
        conn.commit()
        sucNum += 1
    except Exception as e:
        errLog.write(sql + "\r\n" + str(e) + "\r\n")
        errNum += 1   
    
    if totalRow % 1000 == 0:
        print "process " + str(totalRow) + " rows, succ:" + str(sucNum) + ", err:" + str(errNum) + ", rep:" \
        + str(ricRepeat)
        
        
        
        
        
        
        