import time
import os, shutil
from util import custom_chromedriver, custom_logger

# logger 설정
logger = custom_logger.set_logger()

url = 'https://www.avdbs.com/menu/search.php?kwd='
driver_path = 'util/Selenium\\chromedriver.exe'

#chrome driver 설정
driver = custom_chromedriver.set_chromedriver(driver_path)
driver.get('about:blank')
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")

# path_name = 'F:\\점검중'
path_name ='H:\\rarbg\\점검중'

file_list = os.listdir(path_name)

# 생성할 디렉토리를 배열로 받아서 기본 디렉토리 생성
os.chdir(path_name)
output_dirs = {'classified', 'NONE'}

for dir in output_dirs:
    if not(os.path.isdir(dir)):
        os.makedirs(os.path.join(dir))

for temp in file_list:
    if(temp.__eq__('classified')):
        continue
    if (temp.__eq__('NONE')):
        continue

    if(temp.endswith('mp4') == False):
        continue;

    print(temp)

    filename = temp
    temp = temp.replace("\n", "")

    temp = temp.replace("~nyap2p.com.mp4", ".mp4")
    temp = temp.replace("_vip.mfhd.me免 翻 墙 访 问pornhub.mp4", ".mp4")

    temp = temp.replace("-A.mp4", ".mp4")
    temp = temp.replace("-B.mp4", ".mp4")
    temp = temp.replace("-C.mp4", ".mp4")
    temp = temp.replace("-D.mp4", ".mp4")
    temp = temp.replace("-E.mp4", ".mp4")
    temp = temp.replace("-F.mp4", ".mp4")
    temp = temp.replace("-G.mp4", ".mp4")

    temp = temp.replace("CD1_A.mp4", ".mp4")
    temp = temp.replace("CD1_B.mp4", ".mp4")
    temp = temp.replace("CD1_C.mp4", ".mp4")
    temp = temp.replace("CD1_D.mp4", ".mp4")
    temp = temp.replace("CD2_A.mp4", ".mp4")
    temp = temp.replace("CD2_B.mp4", ".mp4")
    temp = temp.replace("CD2_C.mp4", ".mp4")
    temp = temp.replace("CD2_D.mp4", ".mp4")

    temp = temp.replace("A.mp4", ".mp4")
    temp = temp.replace("B.mp4", ".mp4")

    temp = temp.replace("-1.mp4", ".mp4")
    temp = temp.replace("-2.mp4", ".mp4")
    temp = temp.replace("-5.mp4", ".mp4")
    temp = temp.replace("_hd.mp4", ".mp4")
    temp = temp.replace("cd1.mp4", ".mp4")
    temp = temp.replace("cd2.mp4", ".mp4")
    temp = temp.replace("cd3.mp4", ".mp4")
    temp = temp.replace("cd4.mp4", ".mp4")
    temp = temp.replace("CD1.mp4", ".mp4")
    temp = temp.replace("CD2.mp4", ".mp4")
    temp = temp.replace("CD3.mp4", ".mp4")
    temp = temp.replace("CD4.mp4", ".mp4")

    temp = temp.replace(".HD", "")
    temp = temp.replace("21bt.net-", "")
    temp = temp.replace("HD-", "")
    temp = temp.replace("(1080P)@18P2P", "")
    temp = temp.replace("(720P)@18P2P", "")
    temp = temp.replace("big2048.com@", "")

    temp = temp.replace("[44x.me]", "")
    temp = temp.replace("fun2048.com@", "")
    temp = temp.replace("[Thz.la]", "")
    temp = temp.replace("[ThZu.Cc]", "")
    temp = temp.replace("@18P2P", "")
    temp = temp.replace("_uncensored", "")
    temp = temp.replace("[456k.me]", "")
    temp = temp.replace("[Thz.la]", "")
    temp = temp.replace("[ThZu.Cc]", "")
    temp = temp.replace("FHD", "")
    temp = temp.replace("21bt.net-", "")
    temp = temp.replace("-HD", "")
    temp = temp.replace("-h264", "")
    temp = temp.replace("[thz.la]", "")
    temp = temp.replace("1080fhd.com_", "")
    temp = temp.replace("_4K", "")
    temp = temp.replace("-720P", "")


    temp = temp.replace(".mp4", "")
    temp = temp.replace(".avi", "")
    temp = temp.replace(".mkv", "")

    driver.get(url + temp)
    driver.implicitly_wait(1)

    link = '//*[@id="contants"]/ul[2]/li[2]/div/ul/li/div/div[1]/a/img'

    try:
        driver.find_element_by_xpath(link).click()
        actress_name = driver.find_element_by_xpath(
            '//*[@id="ranking_tab1"]/div[1]/div[1]/ul/li[2]/h1/a/span[2]/span[3]').get_attribute('textContent')
        #print(filename + "\t" + actress_name)
        # print("mkdir \"" + actress_name + "\"")
        # print("move " + filename + " \"" + actress_name + "\"")

        print(os.getcwd())
        try:
            os.makedirs(os.path.join(os.getcwd()+'\\classified\\'+actress_name + ""))
        except:
            print()
        shutil.move(filename.replace("\n", ""), "classified\\" + actress_name + "\\" + "" + filename.replace("\n", "") + "")

        # with open('output.txt', 'a') as output_file:
        #     output_file.write("mkdir classified\\\"" + actress_name + "\"" + "\n")
        #     output_file.write("move " + filename.replace("\n", "") + " .\\classified\\\"" + actress_name + "\"\\" + "\n")
    except Exception as e1:
        print(e1)
        #exit()
        # shutil.move(filename.replace("\n", ""), " .\\NONE\\\"" + filename.replace("\n", "") + "\"\\")
        # with open('output.txt', 'a') as output_file:
        #     output_file.write("mkdir NONE" + "\n")
        #     output_file.write("move \"" + filename.replace("\n", "") + "\" .\\NONE\\" + "\n")
    time.sleep(1)

driver.quit()

