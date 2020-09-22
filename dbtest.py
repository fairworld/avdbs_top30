import sqlite3

con = sqlite3.connect('./db/avlist.db')
cur = con.cursor()

# CREATE TABLE "av_list" (
# 	"av_name"	TEXT,
# 	"downloaded"	TEXT,
# 	PRIMARY KEY("av_name")
# );

table_name = 'av_list'

# 테이블을 확인해서 없으면 생성하고 진행
sql = 'SELECT count(name) FROM sqlite_master WHERE type IN (\'table\', \'view\') AND name NOT LIKE \'sqlite_%\' UNION ALL SELECT name FROM sqlite_temp_master WHERE type IN (\'table\', \'view\') and name = \'+table_name+\' ORDER BY 1'
cur.execute(sql)
for row in cur:
    # print(row)
    if row[0] == 0:
        print('av_list 테이블 없으므로 신규 테이블 생성...')
        sql = ' CREATE TABLE "av_list" ( 	"av_name"	TEXT, 	"downloaded"	TEXT, 	PRIMARY KEY("av_name") );'
        cur.execute(sql)
    else:
        print('av_list 테이블 존재하므로 이후 과정 진행...')

sql = 'select av_name, downloaded from av_list where downloaded = \'n\''
cur.execute(sql)
for row in cur:
    print(row[0])
