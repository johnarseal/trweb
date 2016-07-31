# -*- coding: UTF-8 -*-

import MySQLdb,csv,time,os
from dbsettings import *

check1Log = open("check1.log", "a+")
check2Log = open("check2.log", "a+")
check3Log = open("check3.log", "a+")
check4Log = open("check4.log", "a+")

ric2FileDict = {
    "CON.LM":"CON1.LM",
    "PRN.V":"PRN1.V",
    "AUX.WA":"AUX1.WA",
    "CON.L":"CON1.L",
    "AUX.V":"AUX1.V",
    "COM7.BK":"COM71.BK"
}  

file2RicDict = {
    "CON1.LM":"CON.LM",
    "PRN1.V":"PRN.V",
    "AUX1.WA":"AUX.WA",
    "CON1.L":"CON.L",
    "AUX1.V":"AUX.V",
    "COM71.BK":"COM7.BK"
}



liveFolder = [
 u'LiXi',
 u'LIXI2',
 u'LiXi3',
 u'LiXi4',
 u'LiXi5',
 u'LiXi6',
]

# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS,db=DB_NAME)
cur = conn.cursor()

# 1.In filesys but not in path_record
print "Checking In filesys but not in path_record"
lastRecNum = cur.execute("SELECT * FROM " + REC_TBNAME)
rawArr = cur.fetchall()
recArr = [row[0] for row in rawArr]
recDict = {rec:1 for rec in recArr}
# iterate through the directory to insert data from every file
rootDir = u"C:/Users/zz/Google 云端硬盘/lixi"
for folder in liveFolder:
    curDir = os.path.join(rootDir,folder)
    docArr = os.listdir(curDir)
    for doc in docArr:
        suffix = os.path.splitext(doc)[-1]
        if suffix != ".csv":
            continue
        if doc not in recDict:
            check1Log.write(doc + "\n")
            print(doc + " in filesys but not in record")


# 2.In insert_record but not in data table
dataRic = {}
for ind in TB_NAME:
    sql = "SELECT DISTINCT(ric) FROM " + TB_NAME[ind]
    print "Collecting rics from table " + TB_NAME[ind]
    cur.execute(sql)
    raw = cur.fetchall()
    ricArr = [x[0] for x in raw]
    for ric in ricArr:
        if ric not in dataRic:
            dataRic[ric] = 1
            
# do the checking
for doc in recDict:
    ric = doc[:-4]
    if ric not in dataRic:
        if (ric not in file2RicDict) or (file2RicDict[ric] not in dataRic):
            check2Log.write(ric + "\n")
            print(ric + " in path_record but not in data table")            

# 3.In data table but not in path_record
check3errNum = 0
for ric in dataRic:
    doc = ric + ".csv"
    if ric in ric2FileDict:
        doc = ric2FileDict[ric] + ".csv"
        if doc not in recDict:
            check3errNum += 1
            check3Log.write(doc + "\n")
            print(doc + " in data table but not in path_record")

print("Totally find " + str(check3errNum) + " ric error in check3")

# 4.Duplicate in data table
for ind in TB_NAME:
sql = """
    SELECT * FROM tr_ent2ebi_daily a
    WHERE (a.ric,a.ts) IN  (SELECT ric,ts FROM tr_ent2ebi_daily GROUP BY ric,ts  HAVING COUNT(*) > 1)
"""













    print "Checking duplicate in table " + TB_NAME[ind]
    sql = "SELECT COUNT(DISTINCT ric,ts) FROM " + TB_NAME[ind]
    cur.execute(sql)
    distinctNum = cur.fetchall()[0][0]
    sql = "SELECT COUNT(*) FROM " + TB_NAME[ind]
    cur.execute(sql)
    totalNum = cur.fetchall()[0][0]
    check3Log.write("distinct num: " + str(distinctNum) + ", total num: " + str(totalNum) + " in table " + TB_NAME[ind] + "\n")
    print("distinct num: " + str(distinctNum) + ", total num: " + str(totalNum) + " in table " + TB_NAME[ind] + "\n")
