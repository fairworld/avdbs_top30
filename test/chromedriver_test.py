from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(chrome_options=options, executable_path=r'.\Selenium\chromedriver.exe',
                          service_args=["--log-path=./Logs/DubiousDan.log"])
print("Headless Chrome Initialized")
params = {'behavior': 'allow', 'downloadPath': r'.\download'}
driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
driver.get("https://www.mockaroo.com/")
driver.execute_script("scroll(0, 250)");
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#download"))).click()
print("Download button clicked")
# driver.quit()
