# -*- coding: UTF-8 -*-

from dbsettings import *
import MySQLdb

# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS)
cur = conn.cursor()

# create the database
sql = "CREATE DATABASE IF NOT EXISTS trweb"
cur.execute(sql)
cur.execute("USE trweb")

# create table for the daily table
for ind in TB_NAME:
    sql = "CREATE TABLE IF NOT EXISTS " + TB_NAME[ind] + """ (
      `pk` int unsigned AUTO_INCREMENT PRIMARY KEY,
      `ric` varchar(16) NOT NULL DEFAULT '',
      `ts` datetime NOT NULL,
      `trval` decimal(16,6) NULL,
       INDEX  ind_ric(ric)  
    );
    """
    cur.execute(sql)
    
sql = "CREATE TABLE IF NOT EXISTS " + REC_TBNAME + """ (
      `path` varchar(255) PRIMARY KEY
);
"""
cur.execute(sql)

# commit changes
conn.commit()