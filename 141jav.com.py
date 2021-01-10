import os
import re
import sqlite3
import time

import yaml

from util import custom_logger_v2, custom_chromedriver
import download_qbittorrent as dq

if __name__ == '__main__':
    # logger 설정
    filename = re.sub('.py', '.log', os.path.basename(__file__))
    log_dir = os.path.dirname(os.path.realpath(__file__))
    logger = custom_logger_v2.set_logger(log_dir, filename)

    # 변수선언
    with open('conf/data.yml', 'rt', encoding='UTF8') as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    driver_path = conf['driver_path']

    # chrome driver 설정
    # driver = custom_chromedriver.set_chromedriver_headless(driver_path)
    driver = custom_chromedriver.set_chromedriver(driver_path)
    driver.get('about:blank')
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")

    # selenium chromedriver headless download 경로 설정
    custom_chromedriver.enable_download(driver, os.path.join(os.path.dirname(os.path.realpath(__file__)), "download\\"))

    url = 'https://www.141jav.com/popular/?page='

    con = sqlite3.connect('./db/avlist.db')
    cur = con.cursor()
    table_name = 'av_list'

    for i in range(1, 5):
        print(i)
        driver.get(url+i.__str__())
        # break
        torrent_links = driver.find_elements_by_xpath("//A[@class='button is-primary is-fullwidth' and @title='Download .torrent']")
        # torrent_links = driver.find_elements_by_xpath("//A[@class='button is-primary is-fullwidth' and @title='Magnet torrent']")

        # texts = driver.find_elements_by_xpath("//h5//a")
        for text in torrent_links:
            href = text.get_attribute('href')
            title = re.sub('https://www.141jav.com/download/', '', href)
            title = re.sub('.torrent', '', title)

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
                cur.execute(sql, {"Title": title, "Downloaded": 'n', "Url": href})
                logger.info(title + " <= DB Insert 완료")
                con.commit()
            except sqlite3.IntegrityError as ex:
                logger.info(title + "<= 이미 기존에 등록된 항목으로 Pass")
                # print(ex)
                # pass

        time.sleep(10)

    con.commit
    con.close()

    # logger.info("3. 검색된 링크에서 다운로드를 시작합니다.")
    # dq.download(logger)
    # logger.info("작업이 완료되었습니다.")
