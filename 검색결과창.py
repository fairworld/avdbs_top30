import os

import yaml
import sqlite3

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
driver = custom_chromedriver.set_chromedriver(driver_path)
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

'''
Kurokawa Sarina
Koharu Suzuki
Kaname Momojiri
Himawari Yuzuki
Hatsumi Rin
'''

actress_number = '437'
page = 11

for i in range(1, page+1):
    url = 'https://www.avdbs.com/menu/actor.php?actor_idx=' + actress_number + '&_page=' + i.__str__()

    driver.get(url)
    elements = driver.find_elements_by_css_selector('p.snum > a')

    for e in elements:
        title = e.text
        # title로 조회했을 시 이미 데이터가 있는지 확인하는 절차
        try:
            sql = 'select count(title) from av_list where title = :Title'
            cur.execute(sql, {"Title": title})
            for row in cur:
                # 이미 insert된 데이터가 있으면
                if row[0] == 1:
                    continue
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
                    cur.execute(sql, {"Title": title, "Downloaded": 'n', "Url": ''})
                    logger.info(title + ' INSERT 완료')
                    con.commit()
        except:
            logger.info('Exception occured!!!', e)

    time.sleep(10)

con.commit()
con.close()
driver.quit()
driver.close()