from pathlib import Path
from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

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
        self.driver.set_window_size(1920, 1080)
        self.driver.get(SOURCE_PAGE)

    def tearDown(self):
        self.driver.quit()


class TestIDsForDuplicates(TestSelenium, TestCase):
    def test_for_unique_ids(self):
        ids = [x.get_attribute(
            'id') for x in self.driver.find_elements(By.XPATH, '//*[@id]')]
        self.assertEqual(len(ids), len(set(ids)))
