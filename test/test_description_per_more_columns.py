from test.test_description import TestDescription
from unittest import TestCase


class TestDescriptionPerMoreColumns(TestDescription, TestCase):
    def test_more_columns(self):
        self.driver.find_element_by_id(
            'button-for-showing-columns').click()

        self.driver.find_element_by_id(
            'commit-column-selection-input'
        ).find_element_by_xpath('..').click()
        self.columns = "theme, date, stars"
        self.coalesced_text_test()

        self.driver.find_element_by_id(
            'num_stars-column-selection-input'
        ).find_element_by_xpath('..').click()
        self.columns = "theme, date"
        self.coalesced_text_test()

        self.driver.find_element_by_id(
            'date-column-selection-input'
        ).find_element_by_xpath('..').click()
        self.columns = "theme"
        self.coalesced_text_test()

        self.driver.find_element_by_id(
            'cname-column-selection-input'
        ).find_element_by_xpath('..').click()
        self.columns = "theme, date, stars, commit"
        self.coalesced_text_test()

        self.driver.find_element_by_id(
            'min_ver-column-selection-input'
        ).find_element_by_xpath('..').click()
        self.columns = "theme, date, stars, commit, minVer"
        self.coalesced_text_test()

        self.driver.find_element_by_id(
            'license-column-selection-input'
        ).find_element_by_xpath('..').click()
        self.columns = "theme, date, stars, commit, minVer, license"
        self.coalesced_text_test()

        self.driver.find_element_by_id(
            'desc-column-selection-input'
        ).find_element_by_xpath('..').click()
        self.columns = "theme, date, stars, commit, minVer, license, desc"
        self.coalesced_text_test()

        self.driver.find_element_by_id(
            'tags-column-selection-input'
        ).find_element_by_xpath('..').click()
        self.columns = "theme, date, stars, commit, minVer, license, desc, "\
            "tags"
        self.coalesced_text_test()

        self.driver.find_element_by_id(
            'features-column-selection-input'
        ).find_element_by_xpath('..').click()
        self.columns = "theme, date, stars, commit, minVer, license, desc, "\
            "tags, features"
        self.coalesced_text_test()
