import os
import re
import sqlite3
import time
import yaml
from util import custom_chromedriver, init_db, custom_logger_v2

def find_titles(logger):
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
    url_week = conf['url_week']
    url_month = conf['url_month']
    url_year = conf['url_year']
    url_all = conf['url_all']
    url = [url_week, url_month, url_year, url_all]

    driver_path = conf['driver_path']
    user_id = conf['user_id']
    user_password = conf['user_password']
    login_url = conf['login_url']

    # 테이블을 확인해서 없으면 생성하고 진행
    init_db.initialize(logger, cur, table_name)

    # chrome driver 설정
    driver = custom_chromedriver.set_chromedriver_headless(driver_path)
    driver.get('about:blank')
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")

    # selenium chromedriver headless download 경로 설정
    custom_chromedriver.enable_download(driver, os.path.join(os.path.dirname(os.path.realpath(__file__)), "download\\"))

    # 로그인부터 처리
    driver.get(login_url)
    driver.find_element_by_xpath("//*[@id='member_uid']").send_keys(user_id)
    driver.find_element_by_xpath("//*[@id='member_pwd']").send_keys(user_password)
    driver.find_element_by_xpath("//*[@class='btn_login by-avdbs']").click()
    time.sleep(1)

    titles = []
    for u in url:
        driver.get(u)
        elements = driver.find_elements_by_xpath("//*[@class='snum highlight']")

        for e in elements:
            new_title = e.text
            sql = 'select count(title) from av_list where title = ? and downloaded = \'y\''
            cur.execute(sql, (new_title,))
            for row in cur:
                if row[0] == 1:
                    continue
                elif row[0] == 0:
                    titles.append(e.text)

    # set 타입으로 변환하여 중복을 제거, 단 순서는 뒤죽박죽
    titles = set(titles)

    for title in titles:
        try:
            sql = ("insert into "
                   "av_list ("
                   "title, "
                   "downloaded, "
                   "url, "
                   "created_time, "
                   "updated_time) "
                   "values("
                   ":Title, "
                   ":Downloaded, "
                   ":Url, "
                   "datetime(CURRENT_TIMESTAMP, \'localtime\'), "
                   "datetime(CURRENT_TIMESTAMP, \'localtime\'));")
            cur.execute(sql, {"Title": title, "Downloaded": 'n', "Url": ''})
            logger.info(title + " <= DB Insert 완료")
            con.commit()
        except sqlite3.IntegrityError as ex:
            logger.info(title + "<= 이미 기존에 등록된 항목으로 Pass")
            # print(ex)
            # pass

    con.commit()
    con.close()
    driver.close()
    driver.quit()
    return

if __name__ == '__main__':
    find_titles()