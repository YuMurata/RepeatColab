from selenium import webdriver
import config


def init_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-data-dir={config.UserPlofile.dir_path}')
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')

    return webdriver.Chrome('chromedriver', options=options)
