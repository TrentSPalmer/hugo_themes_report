from test.test_description import TestDescription
from unittest import TestCase
import re


class TestDescriptionPerLicense(TestDescription, TestCase):
    def test_description_per_license(self):
        match = re.compile(r'^(.*)(\s\(\d*\))$')

        self.driver.find_element_by_id('button-for-filter-by-license').click()

        licenseSelectionRow = self.driver.find_element_by_id(
            'licenseSelectionRow'
        )

        inputs = [
            x.get_attribute(
                'id'
            ) for x in licenseSelectionRow.find_elements_by_tag_name(
                'input'
            )
        ]

        for i, x in enumerate(inputs):
            button = self.driver.find_element_by_id(
                x).find_element_by_xpath('..')

            license = match.search(
                button.find_element_by_tag_name('label').text).group(1)
            if i == 0:
                self.licenses = license
            else:
                self.licenses += f', {license}'

            button.click()
            self.coalesced_text_test()
