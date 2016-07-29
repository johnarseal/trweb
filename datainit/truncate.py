# -*- coding: UTF-8 -*-

from dbsettings import *
import MySQLdb


# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS,db=DB_NAME)
cur = conn.cursor()

for ind in TB_NAME:
    cur.execute("TRUNCATE TABLE " + TB_NAME[ind])

cur.execute("TRUNCATE TABLE " + REC_TBNAME)

# commit changes
conn.commit()