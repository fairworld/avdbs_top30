
def initialize(logger, cur, table_name):
    # 테이블을 확인해서 없으면 생성하고 진행
    sql = ("SELECT "
           "count(name) "
           "FROM sqlite_master "
           "WHERE type IN (\'table\', \'view\') "
           "AND name NOT LIKE \'sqlite_%\' "
           "UNION ALL "
           "SELECT "
           "name "
           "FROM sqlite_temp_master "
           "WHERE type IN (\'table\', \'view\') "
           "and name = \'"
           +table_name+
           "\' "
           "ORDER BY 1")
    cur.execute(sql)
    for row in cur:
        # print(row)
        if row[0] == 0:
            # print('av_list 테이블 없음')
            logger.info(table_name + ' 테이블 없으므로 생성 진행...')
            sql = ("CREATE "
                   "TABLE "
                   "'av_list' "
                   "('title'	TEXT, "
                   "'downloaded'	TEXT, "
                   "'url'	TEXT, "
                   "'created_time'	TEXT, "
                   "'updated_time'	TEXT, "
                   "'actress'	TEXT, "
                   "PRIMARY KEY('title') );")
            cur.execute(sql)
        else:
            logger.info(table_name + ' 테이블 존재함으로 해당 테이블로 작업 진행...')
