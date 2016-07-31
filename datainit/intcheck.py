# coding=utf-8

import MySQLdb,csv,time,os
from dbsettings import *

import sys
reload(sys) 
sys.setdefaultencoding('utf-8')

check1Log = open("check1.log", "wb")
check2Log = open("check2.log", "wb")

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

"""
# Check 1.In filesys but not in path_record
print "Checking In filesys but not in path_record"
lastRecNum = cur.execute("SELECT * FROM " + REC_TBNAME)
rawArr = cur.fetchall()
recArr = [row[0] for row in rawArr]
recDict = {rec:1 for rec in recArr}
errNum1 = 0

# iterate through the directory to insert data from every file
rootDir = u"C:/Users/zz/Google 云端硬盘/lixi"
for folder in liveFolder:
    curDir = os.path.join(rootDir,folder)
    docArr = os.listdir(curDir)
    for doc in docArr:
        docPair = os.path.splitext(doc)
        suffix = docPair[1]
        if suffix != ".csv":
            continue
        docRic = docPair[0]
        if docRic in file2RicDict:
           docRic = file2RicDict[docRic]
        fullPath = os.path.join(curDir,doc)
        if docRic not in recDict:
            errNum1 += 1
            check1Log.write(fullPath + "\n")
            print(fullPath.encode('gbk') + " in filesys but not in record")
            
print ("total check " + str(errNum1) + " in check1")

"""

# build the ric2path dict
ric2Path = {}
for folder in liveFolder:
    curDir = os.path.join(rootDir,folder)
    docArr = os.listdir(curDir)
    for doc in docArr:
        docPair = os.path.splitext(doc)
        suffix = docPair[1]
        if suffix != ".csv":
            continue  
        # get the file name
        docRic = docPair[0]
        if docRic in file2RicDict:
           docRic = file2RicDict[docRic]
        ric2Path[docRic] = os.path.join(curDir,doc)

# fetch from database
# for insert record
lastRecNum = cur.execute("SELECT * FROM " + REC_TBNAME)
rawArr = cur.fetchall()
recArr = [row[0] for row in rawArr]
recDict = {rec:1 for rec in recArr}
# for ric in database
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
            
# Check 2.In insert_record but not in data table
for ric in recDict:
    if ric not in dataRic:
        check2Log.write(ric + "\r\n")       # for windows
            
"""
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
"""

