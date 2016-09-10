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
noFYLog = open("nofy.log", "w")
# the code starts to run from here   
# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS,db=DB_NAME)
cur = conn.cursor()

num = cur.execute("SELECT DISTINCT(ric) FROM tr_report_annual WHERE fy IS NULL")
print "total " + str(num) + " ric"
raw = cur.fetchall()
for row in raw:
    noFYLog.write(row[0]+"\n")