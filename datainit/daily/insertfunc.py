import csv
# to insert data from a single file into db
def insertSingleFile(filepath,tbName,cursor,retFormat=0):
    errNum = 0
    insertNum = 0
    minVal = 1e-6
    outOfRangeLog = open("outofrange.log", "a+")
    uniqueErrLog = open("uniqueerr.log", "a+")
    uncaughtLog = open("uncaughterr.log", "a+")
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
                        # duplicate
                        tmpTS = time.strftime("%Y-%m-%d",time.strptime(rowArr[i],"%m/%d/%Y"))
                        uKey = str(i+1) + "-" + ric + "-" + tmpTS
                        if uKey in insertRec:
                            continue
                        insertRec[uKey] = 1
                        # out of range
                        if abs(val) < minVal:
                            outOfRangeLog.write(sql + "\n")
                            continue
                        sql = "INSERT INTO " + str(tbName[i+1]) + " (ric, ts, trval) VALUES (" + "'" + ric + "', '" \
                        + tmpTS + "', '" + str(val) + "')"
                        # execute sql
                        try:
                            cursor.execute(sql)
                            insertNum += 1
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
    if retFormat == 0:            
        return errNum
    elif retFormat == 1:
        return (errNum,insertNum)