from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER, logging


def set_chromedriver(driver_path):
    # ChromeDriver 설정
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument('--headless')
    # options.add_argument('windows-size=1920x1080')
    # options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')
    # options.add_argument('--verbose')
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-software-rasterizer')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    options.add_argument('lang=ko_KR')  # 한국어!

    options.add_experimental_option("prefs", {
        # 'download.default_directory': download_path,
        # 'download.prompt_for_download': False,
        # 'download.directory_upgrade': True,
        'safebrowsing_for_trusted_sources_enabled': False,
        'safebrowsing.enabled': False,
        'profile.managed_default_content_settings.images': 2
    })

    driver = webdriver.Chrome(driver_path, options=options)
    # chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
    # driver = webdriver.Chrome(chromedriver_path, options=options)
    return driver


def enable_download(driver, download_dir):
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    driver.execute("send_command", params)
