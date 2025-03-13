import re
from test.test_description import TestDescription
from unittest import TestCase

from selenium.webdriver.common.by import By


class TestDescriptionPerLicense(TestDescription, TestCase):
    def test_description_per_license(self):
        match = re.compile(r'^(.*)(\s\(\d*\))$')

        self.driver.find_element(By.ID, 'button-for-filter-by-license').click()

        licenseSelectionRow = self.driver.find_element(
            By.ID, 'licenseSelectionRow'
        )

        inputs = [
            x.get_attribute(
                'id'
            ) for x in licenseSelectionRow.find_elements(
                By.TAG_NAME, 'input'
            )
        ]

        for i, x in enumerate(inputs):
            button = self.driver.find_element(
                By.ID, x).find_element(By.XPATH, '..')

            license = match.search(
                button.find_element(By.TAG_NAME, 'label').text).group(1)
            if i == 0:
                self.licenses = license
            else:
                self.licenses += f', {license}'

            button.click()
            self.coalesced_text_test()
