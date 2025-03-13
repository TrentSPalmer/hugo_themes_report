import re
from secrets import choice
from test.test_description import TestDescription
from unittest import TestCase

from selenium.webdriver.common.by import By


class TestDescriptionPerFeatures(TestDescription, TestCase):
    def setUp(self):
        super(TestDescriptionPerFeatures, self).setUp()
        self.driver.find_element(By.ID, 'button-for-filter-by-features').click()
        self.match = re.compile(r'^(.*)(\s\(\d*\))$')

    def test_description_per_features(self):
        featureSelectionRow = self.driver.find_element(
            By.ID, 'featureSelectionRow')

        inputs = [
            x.get_attribute(
                'id'
            ) for x in featureSelectionRow.find_elements(
                By.TAG_NAME, 'input'
            )
        ]

        for x in inputs:
            button = self.driver.find_element(
                By.ID, x).find_element(By.XPATH, '..')

            self.features = self.match.search(
                button.find_element(By.TAG_NAME, 'label').text).group(1)

            button.click()
            self.coalesced_text_test()

            self.driver.find_element(
                By.ID, x).find_element(By.XPATH, '..').click()

    def test_description_per_features_random(self):
        self.randomly_select_feature()

    def randomly_select_feature(self):
        featureSelectionRow = self.driver.find_element(
            By.ID, 'featureSelectionRow')

        inputs = [
            x.get_attribute(
                'id'
            ) for x in featureSelectionRow.find_elements(
                By.TAG_NAME, 'input'
            )
        ]

        unchecked_inputs = [
            x for x in inputs if self.driver.find_element(
                By.ID, x).is_selected() is False
        ]

        if len(unchecked_inputs) > 0:
            random_input = choice(unchecked_inputs)
            button = self.driver.find_element(
                By.ID, random_input).find_element(By.XPATH, '..')

            feature = self.match.search(
                button.find_element(By.TAG_NAME, 'label').text).group(1)

            button.click()

            self.assertIn(feature, self.desc.text[158:])
            self.randomly_select_feature()
