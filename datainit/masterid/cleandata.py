from dbsettings import *
import MySQLdb

conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS,db=DB_NAME)
cur = conn.cursor()

sql = "SELECT ric, name, exchange,isin,sector FROM tr_master_id;"

cur.execute(sql)
rawD = cur.fetchall()
ricRepLog = open("ricrepeat.log", "w")
repDict = {}
noISIN = 0
for row in rawD:
    if row[1] == None or row[2] == None:
        continue
    ric = row[0]
    repKey = row[1] + "-" + row[2] + "-" + str(row[3])
    if row[3] == None:
        noISIN += 1
    if repKey not in repDict:
        repDict[repKey] = []
    repDict[repKey].append({"ric":ric,"isin":row[3],"sector":row[4]})

for repKey in repDict:
    if len(repDict[repKey]) > 1:
        for ricRow in repDict[repKey]:
            sql = "SELECT COUNT(*) FROM tr_report_annual WHERE ric = '" + ricRow["ric"] + "'"
            cur.execute(sql)
            recNum = cur.fetchall()[0][0]
            ricRepLog.write(str(recNum) + "," + ricRow["ric"] + "," + str(ricRow["isin"]) + "," + str(ricRow["sector"]) + "," + repKey+"\n")
        
print "NO ISIN:" + str(noISIN)
        
        
        
        
        
        