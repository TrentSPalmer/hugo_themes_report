from test.test_description import TestDescription
from unittest import TestCase

from selenium.webdriver.common.by import By


class TestDescriptionPerMoreColumns(TestDescription, TestCase):
    def test_description_per_more_columns(self):
        self.driver.find_element(By.ID, 'button-for-showing-columns').click()

        self.driver.find_element(
            By.ID, 'commit-column-selection-input'
        ).find_element(By.XPATH, '..').click()
        self.columns = "theme, date, stars"
        self.coalesced_text_test()

        self.driver.find_element(
            By.ID, 'num_stars-column-selection-input'
        ).find_element(By.XPATH, '..').click()
        self.columns = "theme, date"
        self.coalesced_text_test()

        self.driver.find_element(
            By.ID, 'date-column-selection-input'
        ).find_element(By.XPATH, '..').click()
        self.columns = "theme"
        self.coalesced_text_test()

        self.driver.find_element(
            By.ID, 'cname-column-selection-input'
        ).find_element(By.XPATH, '..').click()
        self.columns = "theme, date, stars, commit"
        self.coalesced_text_test()

        self.driver.find_element(
            By.ID, 'min_ver-column-selection-input'
        ).find_element(By.XPATH, '..').click()
        self.columns = "theme, date, stars, commit, minVer"
        self.coalesced_text_test()

        self.driver.find_element(
            By.ID, 'license-column-selection-input'
        ).find_element(By.XPATH, '..').click()
        self.columns = "theme, date, stars, commit, minVer, license"
        self.coalesced_text_test()

        self.driver.find_element(
            By.ID, 'desc-column-selection-input'
        ).find_element(By.XPATH, '..').click()
        self.columns = "theme, date, stars, commit, minVer, license, desc"
        self.coalesced_text_test()

        self.driver.find_element(
            By.ID, 'tags-column-selection-input'
        ).find_element(By.XPATH, '..').click()
        self.columns = "theme, date, stars, commit, minVer, license, desc, "\
            "tags"
        self.coalesced_text_test()

        self.driver.find_element(
            By.ID, 'features-column-selection-input'
        ).find_element(By.XPATH, '..').click()
        self.columns = "theme, date, stars, commit, minVer, license, desc, "\
            "tags, features"
        self.coalesced_text_test()
