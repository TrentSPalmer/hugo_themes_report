from ast import literal_eval
from test.database import get_themes_orderedby_cname
from test.test_filterby_tags import MATCH
from test.test_selenium import TestSelenium
from unittest import TestCase

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


class TestFilterByFeatures(TestSelenium, TestCase):
    def setUp(self):
        super(TestFilterByFeatures, self).setUp()
        for x in [
            'plus-button',
            'button-for-showing-columns',
            'features-column-selection-input',
            'button-for-showing-sort-option',
            'sortByName',
            'button-for-filter-by-features',
        ]:
            self.driver.find_element(By.ID, x).click()

    def test_filterby_features(self):
        filterby_features_inputs = self.get_filter_by_features_inputs()

        for feature in filterby_features_inputs:
            self.driver.find_element(
                By.ID, f"{feature}-feature-selection-input").click()

            self.themes = [x for x in get_themes_orderedby_cname() if
                           x.features_list is not None and feature
                           in literal_eval(x.features_list)]
            self.update_features_available()

            featureSelectionRow = self.driver.find_element(
                By.ID, 'featureSelectionRow')
            buttons = BeautifulSoup(
                featureSelectionRow.get_attribute(
                    'innerHTML'), features='lxml').findAll('button')

            for button in buttons:
                label_text = button.find('label').text
                button_feature = MATCH.search(label_text).group(1)
                button_theme_count = int(MATCH.search(
                    label_text).group(2)[2:-1])
                self.assertEqual(
                    button_theme_count,
                    self.features_available[button_feature]['num_themes']
                )

            results_table_div = self.driver.find_element(By.ID, 'results')
            rows = BeautifulSoup(results_table_div.get_attribute(
                'innerHTML'), features='lxml').find('table').findAll('tr')

            for i, row in enumerate(rows[1:]):
                tds = row.findAll('td')
                tds_txt = [x.text for x in tds]

                self.assertEqual(
                    [
                        tds_txt[0],
                        tds_txt[1],
                        tds_txt[2],
                        tds_txt[3],
                        set(tds_txt[4]),
                    ],
                    [
                        self.themes[i].cname,
                        self.themes[i].commit_date[:10],
                        str(self.themes[i].stargazers_count),
                        self.themes[i].commit_sha[:6],
                        set(','.join(literal_eval(
                            self.themes[i].features_list))),
                    ],
                )

            self.driver.find_element(
                By.ID, f"{feature}-feature-selection-input").click()

    def get_filter_by_features_inputs(self):
        div = self.driver.find_element(By.ID, 'featureSelectionRow')
        return [x.get_attribute('id')[:-24]
                for x in div.find_elements(By.TAG_NAME, 'input')]

    def update_features_available(self):
        self.features_available = {}
        for theme in self.themes:
            for feature in literal_eval(theme.features_list):
                if feature not in self.features_available:
                    self.features_available[feature] = {'num_themes': 1}
                else:
                    self.features_available[feature]['num_themes'] += 1
