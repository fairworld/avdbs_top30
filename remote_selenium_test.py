from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

driver = webdriver.Remote("http://192.168.1.99:4444/wd/hub", DesiredCapabilities.CHROME)
driver.maximize_window()
driver.get("http://clien.net")
