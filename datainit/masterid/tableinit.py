# -*- coding: UTF-8 -*-

from dbsettings import *
import MySQLdb

# connect to database
conn = MySQLdb.connect(host=RAW_HOST,user=RAW_USER,passwd=RAW_PASS)
cur = conn.cursor()

# switch to trweb
cur.execute("USE trweb")

# create table for the daily table
sql = "CREATE TABLE IF NOT EXISTS " + TB_NAME + """ ( 
    `pk` int unsigned AUTO_INCREMENT PRIMARY KEY,
    ric varchar(32) NOT NULL DEFAULT '',
    cusip varchar(12) NULL,
    country varchar(32) NULL,
    exchange varchar(64) NULL,
    industry varchar(100) NULL,
    sub_industry varchar(100) NULL,
    sector varchar(100) NULL,
    isin varchar(16) NULL,
    market_type varchar(24) NULL,
    name varchar(100) NULL,
    sedol varchar(12) NULL,
    status varchar(16) NULL,
    equity varchar(40) NULL,
    ulti_parent varchar(128) NULL,
    UNIQUE ind_ric(ric)  
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
cur.execute(sql)
# commit changes
conn.commit()













