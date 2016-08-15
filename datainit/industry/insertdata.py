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

conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS,db=DB_NAME)
cur = conn.cursor()         

print "creating ricDict"
ricDict = {}
sql = "SELECT ric,industry,sub_industry,sector,country FROM tr_master_id" 
cur.execute(sql)
rawD = cur.fetchall()
for row in rawD:
    ric = row[0]
    if ric not in ricDict:
        ricDict[ric] = {}
    ricDict[ric]["industry"] = row[1]
    ricDict[ric]["sub_industry"] = row[2]
    ricDict[ric]["sector"] = row[3]
    ricDict[ric]["country"] = row[4]

metrics = ("mean","median")
sql = "SELECT COUNT(*) FROM tr_report_annual"
cur.execute(sql)
rowNum = cur.fetchall()[0][0]
step = 10000
tranDict = {}
typeLevel = ["industry","sub_industry","sector","country-industry"]
for rowInd in range(0,rowNum,step):
    print "fetching " + str(rowInd) + " rows"
    sql = "SELECT * FROM tr_report_annual LIMIT " + str(step) + " OFFSET " + str(rowInd)
    cur.execute(sql)
    rawD = cur.fetchall()
    colNum = len(rawD[0])
    for row in rawD:
        ric = row[1]
        ts = row[2]
        if ric not in ricDict:
            continue
        
        ricInfo = {}
        for level in typeLevel:
            if level == "country-industry":
                if ricDict[ric]["country"] != None and ricDict[ric]["industry"] != None:
                    ricInfo[level] = ricDict[ric]["country"] + "-" + ricDict[ric]["industry"]
            else:
                if ricDict[ric][level] != None:
                    ricInfo[level] = ricDict[ric][level]
        
        for level in ricInfo:
            name = ricInfo[level]
            if name not in tranDict:
                tranDict[name] = {"type_level":level,"data":{}}
            
            ts = str(row[2])
            if ts not in tranDict[name]["data"]:
                tranDict[name]["data"][ts] = []
            
            tmp = []
            for ind in range(3,colNum):
                val = row[ind]
                if val != None:
                    val = float(val)
                tmp.append(val)
            tranDict[name]["data"][ts].append(tmp)

"""
for i in tranDict:
    print i
    print tranDict[i]
    for ts in tranDict[i]["data"]:
        print len(tranDict[i]["data"][ts][0])
        break
    break

"""
print "total " + str(len(tranDict)) + " names"
print "calculating"
colNum = 25
cnt = 0
for name in tranDict:
    cnt += 1
    if cnt % 10 == 0:
        print "process " + str(cnt) + " names"
    tranDict[name]["stat"] = {}
    for ts in tranDict[name]["data"]:
        tranDict[name]["stat"][ts] = {"median":{},"mean":{}}
        
        rowNum = len(tranDict[name]["data"][ts])
        mat = tranDict[name]["data"][ts]
        rotMat = {}
        for i in range(colNum):
            rotMat[i] = []
            for j in range(rowNum):
                if mat[j][i] != None:
                    rotMat[i].append(mat[j][i])
        
        
        for ind in rotMat:
            tmpLen = len(rotMat[ind])
            if tmpLen == 0:
                tranDict[name]["stat"][ts]["mean"][ind] = 0
                tranDict[name]["stat"][ts]["median"][ind] = 0
                continue
            rotMat[ind].sort()
            tranDict[name]["stat"][ts]["mean"][ind] = sum(rotMat[ind]) / tmpLen
            tranDict[name]["stat"][ts]["median"][ind] = rotMat[ind][int(tmpLen / 2)]
        
print "inserting"   
for name in tranDict
    for ts in tranDict[name]["stat"]:
        pair = tranDict[name]["stat"][ts]
        for metric in pair:
            sql = "INSERT INTO tr_industry_sum (name,type_level,stat"
        
        
    tranDict[name]["stat"]
conn.commit()

       
