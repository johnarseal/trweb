# -*- coding: UTF-8 -*-

import MySQLdb,csv,time,os,math,signal,sys
from dbsettings import *

# the files for manually log
outOfRangeLog = open("outofrange.log", "a+")
uniqueErrLog = open("uniqueerr.log", "a+")
recordErrLog = open("recorderr.log", "a+")
uncaughtLog = open("uncaughterr.log", "a+")

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


# to insert data from a single file into db
def insertSingleFile(filepath,tbName,cursor):
    errNum = 0
    minVal = 1e-6
    with open(filepath,"r") as csvfile:
        cnt = 0
        insertRec = {}
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
                        # nan
                        if math.isnan(val):
                            continue
                        # out of range
                        if abs(val) < minVal:
                            outOfRangeLog.write(sql + "\n")
                            continue
                        # duplicate
                        tmpTS = time.strftime("%Y-%m-%d",time.strptime(rowArr[i],"%m/%d/%Y"))
                        uKey = str(i+1) + "-" + ric + "-" + tmpTS
                        if uKey in insertRec:
                            continue
                        insertRec[uKey] = 1
                        sql = "INSERT INTO " + str(tbName[i+1]) + " (ric, ts, trval) VALUES (" + "'" + ric + "', '" \
                        + tmpTS + "', '" + str(val) + "')"
                        # execute sql
                        try:
                            cursor.execute(sql)
                        except Exception as e:
                            if type(e).__name__ == "IntegrityError":
                                uniqueErrLog.write(sql + "\n")
                            elif type(e).__name__ == "DataError":
                                outOfRangeLog.write(sql + "\n")
                            else:
                                errNum += 1
                                uncaughtLog.write(str(e) + "\n" + sql + "\n")
                            continue
                            
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

# start to insert data
print ("Start to insert file, already insert " + str(lastRecNum) + " files")
print ("Time now: " + str(time.clock()))
# iterate through the directory to insert data from every file
rootDir = u"C:/Users/zz/Google 云端硬盘/lixi"
pathArr = os.listdir(rootDir)
liveFolder = [
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
        docCnt += 1
        if docRic in lastRecDict:
            continue
            
        curDoc = os.path.join(curDir,doc)            
        curRecord.append(docRic)
        totalErr += insertSingleFile(curDoc,TB_NAME,cur)
        # for every 50 documents, commit a change
        if docCnt % 50 == 0:
            print ("Handled " + str(docCnt) + " file, Uncaught insert err: " + str(totalErr))
            print ("Time: " + str(time.clock()))
            
            for docRic in curRecord:
                sql = "INSERT INTO " + REC_TBNAME + " VALUES ('" + docRic + "')"
                try:
                    cur.execute(sql)
                except Exception as e:
                    recordErrLog.write(str(e) + "\n" + sql + "\n")           
            
            conn.commit()
            curRecord = []



