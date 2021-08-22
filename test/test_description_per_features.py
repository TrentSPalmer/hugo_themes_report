from test.test_description import TestDescription
from unittest import TestCase
from secrets import choice
import re


class TestDescriptionPerFeatures(TestDescription, TestCase):
    def setUp(self):
        super(TestDescriptionPerFeatures, self).setUp()
        self.driver.find_element_by_id('button-for-filter-by-features').click()
        self.match = re.compile(r'^(.*)(\s\(\d*\))$')

    def test_description_per_features(self):
        featureSelectionRow = self.driver.find_element_by_id(
            'featureSelectionRow')

        inputs = [
            x.get_attribute(
                'id'
            ) for x in featureSelectionRow.find_elements_by_tag_name(
                'input'
            )
        ]

        for x in inputs:
            button = self.driver.find_element_by_id(
                x).find_element_by_xpath('..')

            self.features = self.match.search(
                button.find_element_by_tag_name('label').text).group(1)

            button.click()
            self.coalesced_text_test()

            self.driver.find_element_by_id(
                x).find_element_by_xpath('..').click()

    def test_description_per_features_random(self):
        self.randomly_select_feature()

    def randomly_select_feature(self):
        featureSelectionRow = self.driver.find_element_by_id(
            'featureSelectionRow')

        inputs = [
            x.get_attribute(
                'id'
            ) for x in featureSelectionRow.find_elements_by_tag_name(
                'input'
            )
        ]

        unchecked_inputs = [
            x for x in inputs if self.driver.find_element_by_id(
                x).is_selected() is False
        ]

        if len(unchecked_inputs) > 0:
            random_input = choice(unchecked_inputs)
            button = self.driver.find_element_by_id(
                random_input).find_element_by_xpath('..')

            feature = self.match.search(
                button.find_element_by_tag_name('label').text).group(1)

            button.click()

            self.assertIn(feature, self.desc.text[-15:])
            self.randomly_select_feature()
