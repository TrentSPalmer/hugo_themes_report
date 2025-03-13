from test.test_description import TestDescription
from unittest import TestCase

from selenium.webdriver.common.by import By


class TestDescriptionPerSortBy(TestDescription, TestCase):
    def setUp(self):
        super(TestDescriptionPerSortBy, self).setUp()
        self.driver.find_element(
            By.ID, 'button-for-showing-sort-option').click()

    def test_description_per_sort_by_stars(self):
        self.driver.find_element(
            By.ID, 'sortByStars'
        ).find_element(By.XPATH, '..').click()
        self.sorted_by = "stars, date, name, minVer, license"
        self.coalesced_text_test()

    def test_description_per_sort_by_License(self):
        self.driver.find_element(
            By.ID, 'sortByLicense'
        ).find_element(By.XPATH, '..').click()
        self.sorted_by = "license, date, stars, name, minVer"
        self.coalesced_text_test()

    def test_description_per_sort_by_minVer(self):
        self.driver.find_element(
            By.ID, 'sortByMinVer'
        ).find_element(By.XPATH, '..').click()
        self.sorted_by = "minVer, date, stars, name, license"
        self.coalesced_text_test()

    def test_description_per_sort_by_name(self):
        self.driver.find_element(
            By.ID, 'sortByName'
        ).find_element(By.XPATH, '..').click()
        self.sorted_by = "name, date, stars, minVer, license"
        self.coalesced_text_test()
