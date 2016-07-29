# -*- coding: UTF-8 -*-

import MySQLdb,csv,time,os,math,signal,sys
from dbsettings import *


# to insert data from a single file into db
def insertSingleFile(filepath,tbName,cursor):
    errNum = 0
    with open(filepath,"r") as csvfile:
        cnt = 0
        minVal = 1e-6
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for rowArr in spamreader:
            cnt += 1
            if cnt == 1:
                ric = rowArr[0]
                numCol = len(rowArr)
            elif cnt == 2:
                continue
            else:
                for i in range(0,numCol,2):
                    try:
                        val = round(float(rowArr[i+1]),6)
                        # filter out invalid data
                        if abs(val) < minVal or math.isnan(val):
                            continue
                        sql = "INSERT INTO " + str(tbName[i+1]) + " (ric, ts, trval) VALUES (" + "'" + ric + "', '" \
                        + time.strftime("%Y-%m-%d",time.strptime(rowArr[i],"%m/%d/%Y")) + "', '" + str(val) + "')"
                        # execute sql       
                        try:
                            cursor.execute(sql)
                        except Exception as e:
                            errNum += 1
                            print (sql)
                            print (e)
                    except:
                        continue
                
    return errNum

# the code starts to run from here   
# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS,db=DB_NAME)
cur = conn.cursor()

# when the console is terminated, roll back transaction
def term_sig_handler(signum, frame):  
    print 'catched singal: %d' % signum
    print "rolling back transactions"
    conn.rollback()
    sys.exit()  

# register the terminate signal handler
signal.signal(signal.SIGTERM, term_sig_handler)  
signal.signal(signal.SIGINT, term_sig_handler)  

# fetch the record of the files that have been already inserted
lastRecNum = cur.execute("SELECT * FROM " + REC_TBNAME)
rawArr = cur.fetchall()
recArr = [row[0] for row in rawArr]
lastRecDict = {rec:1 for rec in recArr}
print ("Start to insert file, already insert " + str(lastRecNum) + " files")
print ("Time now: " + str(time.clock()))
# iterate through the directory to insert data from every file
rootDir = u"C:/Users/zz/Google 云端硬盘/lixi"
pathArr = os.listdir(rootDir)
curReady = [
 u'LiXi',
 u'LIXI2',
 u'LiXi3',
 u'LiXi4',
 u'LiXi5',
 u'LiXi6',
]

docCnt = 0
totalErr = 0
curRecord = []

for folder in curReady:
    curDir = os.path.join(rootDir,folder)
    docArr = os.listdir(curDir)
    for doc in docArr:
        suffix = os.path.splitext(doc)[-1]
        if suffix != ".csv":
            continue
        docCnt += 1
        curDoc = os.path.join(curDir,doc)
        if curDoc in lastRecDict:
            continue
        curRecord.append(doc)
        totalErr += insertSingleFile(curDoc,TB_NAME,cur)
        # for every 50 documents, commit a change
        if docCnt % 50 == 0:
            print ("Handled " + str(docCnt) + " file, Total error: " + str(totalErr))
            print ("Time: " + str(time.clock()))
            
            for docName in curRecord:
                cur.execute("INSERT INTO " + REC_TBNAME + " VALUES ('" + docName + "')")            
            
            conn.commit()
            curRecord = []




