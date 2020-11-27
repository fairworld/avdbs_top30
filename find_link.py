import os
import re
import sqlite3
import time
import yaml
from util import custom_chromedriver, init_db, custom_logger_v2

def find_link(logger):
    # logger 설정
    # logger = custom_logger_v2.set_logger(os.path.dirname(os.path.realpath(__file__)),
    #                                      re.sub('.py', '.log', os.path.basename(__file__)))

    # sqlite3 db 연결
    # 로그 저장할 폴더 생성
    db_dir = '{}/db'.format(os.path.dirname(os.path.realpath(__file__)))
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    con = sqlite3.connect('./db/avlist.db')
    cur = con.cursor()
    table_name = 'av_list'

    # 변수선언
    with open('conf/data.yml', 'rt', encoding='UTF8') as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)

    driver_path = conf['driver_path']


    # 테이블을 확인해서 없으면 생성하고 진행
    init_db.initialize(logger, cur, table_name)

    # chrome driver 설정
    driver = custom_chromedriver.set_chromedriver_headless(driver_path)
    driver.get('about:blank')
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")

    # selenium chromedriver headless download 경로 설정
    custom_chromedriver.enable_download(driver, os.path.join(os.path.dirname(os.path.realpath(__file__)), "download\\"))

    # 기존 목록에서 다운로드 실패한 내역을 갖고 와서 검색할 품번에 추가
    titles = []
    sql = 'select title, downloaded from av_list where downloaded = \'n\''
    cur.execute(sql)
    for row in cur:
        titles.append(row[0])

    url = 'https://sukebei.nyaa.si/?f=0&c=0_0&s=seeders&o=desc&q='

    # set 타입으로 변환하여 중복을 제거, 단 순서는 뒤죽박죽
    titles = set(titles)
    total_count = len(titles)

    count = 0
    iteration = 0
    for title in titles:
        driver.get(url + title)
        iteration += 1
        count_str = str(iteration) + "/" + str(total_count)
        try:
            download_url = driver.find_element_by_xpath("//td[@class='text-center']/a").get_attribute('href')
            try:
                sql = ("UPDATE "
                       "av_list "
                       "SET downloaded = :Downloaded, "
                       "updated_time = datetime(CURRENT_TIMESTAMP, \'localtime\'), "
                       "url = :Url "
                       "WHERE title = :Title")
                cur.execute(sql, {"Downloaded": 'y', "Url": download_url, "Title": title})
                logger.info(count_str + " " + title + "(" + download_url + ") <= URL을 DB Insert 완료")
                con.commit()
            except:
                # logger.info(count_str + " " + title + " <= URL을 찾을 수 없음")
                pass
        except:
            logger.info(count_str + " " + title + " <= URL을 찾을 수 없음")
            # pass
        count = count + 1
        time.sleep(1)

    logger.info('총 ' + len(titles).__str__() + '건 중 ' + count.__str__() + '건을 신규로 URL을 추가하였습니다.')
    con.commit()
    con.close()
    # time.sleep(10)
    driver.close()
    driver.quit()
    return

if __name__ == '__main__':
    find_link()