import time
import sqlite3
import custom_logger
import custom_chromedriver

# logger 설정
logger = custom_logger.set_logger()

# sqlite3 db 연결
con = sqlite3.connect('../db/avlist.db')
cur = con.cursor()
table_name = 'av_list'

# 테이블을 확인해서 없으면 생성하고 진행
sql = 'SELECT count(name) FROM sqlite_master WHERE type IN (\'table\', \'view\') AND name NOT LIKE \'sqlite_%\' UNION ALL SELECT name FROM sqlite_temp_master WHERE type IN (\'table\', \'view\') and name = \'+table_name+\' ORDER BY 1'
cur.execute(sql)
for row in cur:
    # print(row)
    if row[0] == 0:
        # print('av_list 테이블 없음')
        sql = 'CREATE TABLE "av_list" ( "title"	TEXT, "downloaded"	TEXT, "url"	TEXT, "created_time"	TEXT, "updated_time"	TEXT, PRIMARY KEY("title") );'
        cur.execute(sql)

# 변수설정
url_week = 'https://www.avdbs.com/menu/dvd_ranking.php'
url_month = 'https://www.avdbs.com/menu/dvd_ranking.php?tab=month'
url_year = 'https://www.avdbs.com/menu/dvd_ranking.php?tab=year'
url_all = 'https://www.avdbs.com/menu/dvd_ranking.php?tab=all'

# url = [url_week, url_month, url_year, url_all]
url = [url_week,url_month,url_year,url_all]

driver_path = 'Selenium\\chromedriver.exe'
user_id = 'fairworld'
user_password = 'wjds$1029!'
login_url = 'https://www.avdbs.com/menu/member/login.php'

#chrome driver 설정
driver = custom_chromedriver.set_chromedriver(driver_path)
driver.get('about:blank')
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")

#로그인부터 처리
driver.get(login_url)
driver.find_element_by_xpath("//*[@id='member_uid']").send_keys(user_id)
driver.find_element_by_xpath("//*[@id='member_pwd']").send_keys(user_password)
driver.find_element_by_xpath("//*[@class='btn_login by-avdbs']").click()
time.sleep(1)

titles = []
for u in url:
    driver.get(u)
    elements = driver.find_elements_by_xpath("//*[@class='snum highlight']")

    # print('목록에 올라온 수량: ' + len(elements))

    for e in elements:
        new_title = e.text
        sql = 'select count(title) from av_list where title = ? and downloaded = \'y\''
        cur.execute(sql, (new_title,))
        for row in cur:
            if row[0] == 1:
                continue;
            elif row[0] == 0:
                titles.append(e.text)

# set 타입으로 변환하여 중복을 제거, 단 순서는 뒤죽박죽
titles = set(titles)

# for t in titles:
#     print(t)

# 기존 목록에서 다운로드 실패한 내역을 갖고 와서 검색할 품번에 추가
# sql = 'select title, downloaded from av_list where downloaded = \'n\''
# cur.execute(sql)
# for row in cur:
#     titles.append(row[0])

url2 = 'https://sukebei.nyaa.si/?f=0&c=0_0&s=size&o=desc&q='

logger.info('기존 미다운로드 수량과 목록 수량을 합한 량: ' + len(titles).__str__())
total_count = len(titles)

count = 0
failure = 0
for title in titles:
    logger.debug(title)
    driver.get(url2 + title)
    count +=  1
    try:
        download_url = driver.find_element_by_xpath("//td[@class='text-center']/a").get_attribute('href')
        logger.debug(download_url)
        driver.find_element_by_xpath("//td[@class='text-center']/a").click()
        logger.info(count.__str__() + "/" + total_count.__str__() + "\t" + title + "(" + download_url + ") <= 다운로드 완료")
        try:
            cur.execute('insert into av_list values(?, ?, ?, datetime(CURRENT_TIMESTAMP, \'localtime\'), datetime(CURRENT_TIMESTAMP, \'localtime\'));', (title, 'y', download_url))
            con.commit()
        except Exception as e1:
            print('1st exception')
            print(e)
            cur.execute("UPDATE av_list SET downloaded = ?, updated_time = datetime(CURRENT_TIMESTAMP, \'localtime\'), url = ? WHERE title = ?", ('y', title, download_url))
            con.commit()

    except Exception as e1:
        try:
            logger.info(count.__str__() + "/" + total_count.__str__() + "\t" + title + " <= Seed 없음")
            failure = failure + 1
            cur.execute('insert into av_list values(?, ?, ?, datetime(CURRENT_TIMESTAMP, \'localtime\'), datetime(CURRENT_TIMESTAMP, \'localtime\'));', (title, 'n', ''))
            con.commit()
        except Exception as e:
            print('2nd exception')
            print(e)
            continue;
        print('3rd exception')
        print(e1)
        continue;

success = len(titles) - failure

logger.info('총 ' + len(titles).__str__() + '건 중 ' + str(success) + '건을 신규로 다운로드 완료하였습니다.')
con.commit()
con.close()
time.sleep(10)
driver.close()
