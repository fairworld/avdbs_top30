import os

import yaml
import sqlite3

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from util import custom_chromedriver, init_db, custom_logger
import time


'''
# To do list
1. ch로 끝나는 파일을 확인할 방법이 있는가?
'''

# logger 설정
log_dir = os.path.dirname(os.path.realpath(__file__))
logger = custom_logger.set_logger(log_dir)

# sqlite3 db 연결
# 로그 저장할 폴더 생성
current_dir = os.path.dirname(os.path.realpath(__file__))
db_dir = '{}/db'.format(current_dir)
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
# url = [url_week,]

driver_path = conf['driver_path']
user_id = conf['user_id']
user_password = conf['user_password']
login_url = conf['login_url']

# 테이블을 확인해서 없으면 생성하고 진행
init_db.initialize(logger, cur, table_name)

# chrome driver 설정
# driver = custom_chromedriver.set_chromedriver(driver_path)
driver = webdriver.Remote("http://192.168.1.99:4444/wd/hub", DesiredCapabilities.CHROME)
driver.get('about:blank')
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")

# selenium chromedriver headless download 경로 설정
custom_chromedriver.enable_download(driver, "/home/seluser/")

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

# 기존 목록에서 다운로드 실패한 내역을 갖고 와서 검색할 품번에 추가
sql = 'select title, downloaded from av_list where downloaded = \'n\''
cur.execute(sql)
for row in cur:
    titles.append(row[0])

url2 = 'https://sukebei.nyaa.si/?f=0&c=0_0&s=size&o=desc&q='
#url2 = 'https://sukebei.nyaa.si/?f=0&c=0_0&s=seeders&o=desc&q='


# set 타입으로 변환하여 중복을 제거, 단 순서는 뒤죽박죽
titles = set(titles)

logger.info('기존 미다운로드 수량과 목록 수량을 합한 량: ' + len(titles).__str__())
total_count = len(titles)

count = 0
iteration = 0
for title in titles:
    driver.get(url2 + title)
    iteration += 1
    count_str = str(iteration) + "/" + str(total_count)
    try:
        download_url = driver.find_element_by_xpath("//td[@class='text-center']/a").get_attribute('href')
        driver.find_element_by_xpath("//td[@class='text-center']/a").click()
        logger.info(count_str + " " + title + "(" + download_url + ") <= 다운로드 완료")

        # title로 조회했을 시 이미 데이터가 있는지 확인하는 절차
        try:
            sql = 'select count(title) from av_list where title = :Title'
            cur.execute(sql, {"Title": title})
            for row in cur:
                # 이미 insert된 데이터가 있으면
                if row[0] == 1:
                    sql = ("UPDATE "
                           "av_list "
                           "SET downloaded = :Downloaded, "
                           "updated_time = datetime(CURRENT_TIMESTAMP, \'localtime\'), "
                           "url = :Url "
                           "WHERE title = :Title")
                    cur.execute(sql, {"Downloaded": 'y', "Url": download_url, "Title": title})
                    logger.info('UPDATE 완료')
                    con.commit()
                # 아직 insert된 데이터가 없으면
                elif row[0] == 0:
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
                    cur.execute(sql, {"Title": title, "Downloaded": 'y', "Url": download_url})
                    logger.info('INSERT 완료')
                    con.commit()
            count = count + 1
        except:
            # logger.info('Exception occured!!!', e)
            logger.info(count_str + " " + title + "<= DB INSERT 실패")
    except:
        try:
            logger.info(count_str + " " + title + " <= Seed 없음")
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
            con.commit()
        except:
            # logger.info('Exception occured!!!', e)
            logger.info(count_str + " " + title + "<= DB INSERT 실패")
            con.commit()
            continue
        continue

    # time.sleep(1)

logger.info('총 ' + len(titles).__str__() + '건 중 ' + count.__str__() + '건을 신규로 다운로드 완료하였습니다.')
con.commit()
con.close()
time.sleep(10)
driver.close()
driver.quit()