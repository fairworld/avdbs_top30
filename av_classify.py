import time
import os, shutil
from util import custom_chromedriver, custom_logger
from datetime import datetime

# dateformat 설정
datestr_format = "{:%Y-%m-%d_%H%M%S}"
datestr = datestr_format.format(datetime.now())

# logger 설정
log_dir = os.path.dirname(os.path.realpath(__file__))
logger = custom_logger.set_logger(log_dir)

url = 'https://www.avdbs.com/menu/search.php?kwd='
driver_path = 'util/Selenium\\chromedriver.exe'

# chrome driver 설정
driver = custom_chromedriver.set_chromedriver(driver_path)
driver.get('about:blank')
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")

path_name = 'D:\\점검중'
# path_name ='F:\\rarbg\\점검중'

file_list = os.listdir(path_name)

# 생성할 디렉토리를 배열로 받아서 기본 디렉토리 생성
os.chdir(path_name)
output_dirs = {datestr}

for d in output_dirs:
    if not (os.path.isdir(d)):
        os.makedirs(os.path.join(d))

for temp in file_list:
    if temp.__eq__(datestr):
        continue

    if not temp.endswith(('mp4', 'wmv', 'avi', 'mkv')):
        continue

    print(temp)

    filename = temp
    temp = temp.replace("\n", "")
    temp = temp.replace(".mp4", "")
    temp = temp.replace(".avi", "")
    temp = temp.replace(".mkv", "")
    temp = temp.replace(".wmv", "")

    driver.get(url + temp)
    driver.implicitly_wait(1)

    link = '//*[@id="contants"]/ul[2]/li[2]/div/ul/li/div/div[1]/a/img'

    try:
        driver.find_element_by_xpath(link).click()
        actress_name = driver.find_element_by_xpath(
            '//*[@id="ranking_tab1"]/div[1]/div[1]/ul/li[2]/h1/a/span[2]/span[3]').get_attribute('textContent')

        print(os.getcwd())
        try:
            os.makedirs(os.path.join(os.getcwd() + '\\' + datestr + '\\' + actress_name + ""))
        except:
            print()
        shutil.move(filename.replace("\n", ""),
                    datestr+ "\\" + actress_name + "\\" + "" + filename.replace("\n", "") + "")

    except Exception as e1:
        print(e1)
    time.sleep(1)

driver.quit()
