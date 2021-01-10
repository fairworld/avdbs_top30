import os
import re
from turtle import down

import yaml
import sqlite3

from util import custom_chromedriver, init_db, custom_logger_v2
from qbittorrent import Client


def download(logger):
    # logger 설정
    # filename = re.sub('.py', '.log', os.path.basename(__file__))
    # log_dir = os.path.dirname(os.path.realpath(__file__))
    # logger = custom_logger_v2.set_logger(log_dir, filename)

    con = sqlite3.connect('db/avlist.db')
    cur = con.cursor()
    table_name = 'av_list'

    # 변수선언
    with open('conf/data.yml', 'rt', encoding='UTF8') as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)

    qburl = conf['qburl']
    qbid = conf['qbid']
    qbpwd = conf['qbpwd']

    # qBittorrent 연결
    qb = Client(qburl)
    qb.login(qbid, qbpwd)

    # 미 다운로드 목록을 조회
    urls = []
    try:
        sql = "select title, url from av_list where qbittorrent_add = 'n' and url <> ''"
        cur.execute(sql)
        rows = cur.fetchall()
        # print(len(rows))
        for row in rows:
            urls.append((row[0], row[1]))

    except:
        logger.info("쿼리 실패")

    total_count = len(urls)
    count = 0

    for u in urls:
        logger.info("TITLE : " + u[0] + "\t\t" + "URL : " + u[1])
        try:
            qb.download_from_link(u[1])
            logger.info(u[0] + "\t" + "다운로드 요청 전송 성공")
            sql = "update av_list set qbittorrent_add = 'y' where title = '" + u[0] + "'"
            con.execute(sql)
            count += 1
            # print(sql)
        except Exception as ex:
            logger.info(u[0] + "\t" + "다운로드 요청 전송 실패")
            logger.error(ex)

    logger.info("총 " + total_count.__str__() + "건 중 " + count.__str__() + "건을 신규로 다운로드 요청하였습니다.")

    con.commit()
    con.close()
    return

if __name__ == '__main__':
    # logger 설정
    filename = re.sub('.py', '.log', os.path.basename(__file__))
    log_dir = os.path.dirname(os.path.realpath(__file__))
    logger = custom_logger_v2.set_logger(log_dir, filename)
    download(logger)