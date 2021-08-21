from unittest import TestCase
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
OPTIONS = Options()
OPTIONS.add_argument('--ignore-certificate-errors')
OPTIONS.add_argument('--incognito')
OPTIONS.add_argument('--headless')
SERVICE = Service('/usr/bin/chromedriver')
SOURCE_FILE = Path('hugo-themes-report/hugo-themes-report.html').resolve()
SOURCE_PAGE = f'file://{str(SOURCE_FILE)}'


class TestSelenium(TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(options=OPTIONS, service=SERVICE)
        self.driver.get(SOURCE_PAGE)

    def tearDown(self):
        self.driver.quit()
