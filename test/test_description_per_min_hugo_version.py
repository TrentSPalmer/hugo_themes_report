from test.test_description import TestDescription
from unittest import TestCase

from selenium.webdriver.common.by import By


class TestDescriptionPerMinHugoVersion(TestDescription, TestCase):
    def test_description_per_min_hugo_version(self):

        self.driver.find_element(By.ID, 'button-for-filter-by-minver').click()

        minVerSelectionRow = self.driver.find_element(
            By.ID, 'minVerSelectionRow'
        )

        inputs = [
            x.get_attribute(
                'id'
            ) for x in minVerSelectionRow.find_elements(
                By.TAG_NAME, 'input'
            )
        ]

        for x in inputs:
            button = self.driver.find_element(
                By.ID, x).find_element(By.XPATH, '..')

            self.min_ver = button.find_element(By.TAG_NAME, 'label').text

            button.click()
            self.coalesced_text_test()
