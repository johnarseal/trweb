# -*- coding: UTF-8 -*-

from dbsettings import *
import MySQLdb,xlrd

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

# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS)
cur = conn.cursor()
cur.execute("use trweb")

filePath = 'C:/project/Lixi/raw/new ID file interface.xlsx'
curSH = openSH(filePath,"new ID file")
numRow = curSH.nrows
numCol = curSH.ncols
for i in range(1,numRow):
    sector = curSH.cell_value(i,8)
    if sector != "NULL" and sector != "":
        ric = curSH.cell_value(i,1)
        sql = "UPDATE tr_master_id SET sector = '" + str(sector) + "' WHERE ric = '" + str(ric) + "'"
        try:
            cur.execute(sql)
            
        except Exception as e:
            print sql
            print e
    if i % 10000 == 0:
        print "handle " + str(i) + " rows"
        conn.commit()