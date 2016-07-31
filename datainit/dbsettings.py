# coding=utf-8

# seetings for the database
RAW_HOST = 'localhost'
RAW_USER = 'root'
RAW_PASS = ''
DB_NAME = 'trweb'
REC_TBNAME = 'tr_insert_record'
TB_NAME = {
                3:"tr_peratio_daily",
                5:"tr_price2cf_daily",
                7:"tr_ent2ebi_daily",
                9:"tr_percentch_daily",
                11:"tr_priclose_daily",
                13:"tr_weektotret_daily",
                15:"tr_monthtotret_daily"
           }
           
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

rootDir = u"C:/Users/zz/Google 云端硬盘/lixi"
liveFolder = [
 u'LiXi',
 u'LIXI2',
 u'LiXi3',
 u'LiXi4',
 u'LiXi5',
 u'LiXi6',
]