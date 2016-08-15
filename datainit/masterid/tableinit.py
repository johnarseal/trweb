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
    ric varchar(32) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL DEFAULT '' UNIQUE,
    cusip varchar(12) NULL,
    country varchar(32) NULL,
    exchange varchar(100) NULL,
    industry varchar(100) NULL,
    sub_industry varchar(100) NULL,
    sector varchar(100) NULL,
    isin varchar(16) NULL,
    market_type varchar(24) NULL,
    name varchar(128) NULL,
    sedol varchar(12) NULL,
    status varchar(16) NULL,
    equity varchar(40) NULL,
    ulti_parent varchar(128) NULL,
    company_ticker varchar(32) NULL,
    mifid boolean NULL,
    shariah boolean NULL,
    market_cap bigint unsigned NULL,
    currency varchar(32) NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
cur.execute(sql)
# commit changes
conn.commit()













