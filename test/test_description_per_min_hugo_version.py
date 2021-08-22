from test.test_description import TestDescription
from unittest import TestCase


class TestDescriptionPerMinHugoVersion(TestDescription, TestCase):
    def test_description_per_min_hugo_version(self):

        self.driver.find_element_by_id('button-for-filter-by-minver').click()

        minVerSelectionRow = self.driver.find_element_by_id(
            'minVerSelectionRow'
        )

        inputs = [
            x.get_attribute(
                'id'
            ) for x in minVerSelectionRow.find_elements_by_tag_name(
                'input'
            )
        ]

        for x in inputs:
            button = self.driver.find_element_by_id(
                x).find_element_by_xpath('..')

            self.min_ver = button.find_element_by_tag_name('label').text

            button.click()
            self.coalesced_text_test()
