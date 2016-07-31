# coding=utf-8
import os
from dbsettings import * 

deadlog = open("live_dead_ric.log", "wb")


for folder in liveFolder:
    curDir = os.path.join(rootDir,folder)
    docArr = os.listdir(curDir)
    for doc in docArr:
        docPair = os.path.splitext(doc)
        docRic = docPair[0]
        deadlog.write(docRic + "\r\n")