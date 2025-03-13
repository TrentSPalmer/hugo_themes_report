from test.database import get_themes_orderedby_cname
from test.test_selenium import TestSelenium
from unittest import TestCase

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


class TestFilterByLicense(TestSelenium, TestCase):
    def setUp(self):
        super(TestFilterByLicense, self).setUp()
        for x in [
                'plus-button',
                'button-for-showing-columns',
                'license-column-selection-input',
                'button-for-showing-sort-option',
                'sortByName',
                'button-for-filter-by-license',
        ]:
            self.driver.find_element(By.ID, x).click()
        self.themes = get_themes_orderedby_cname()

    def test_filter_by_license(self):
        filterby_lic_inputs = [x.get_attribute('id')[:-24]
                               for x in self.driver.find_element(
            By.ID, 'licenseSelectionRow').find_elements(By.TAG_NAME, 'input')]

        for license in filterby_lic_inputs:
            self.driver.find_element(
                By.ID, f"{license}-license-selection-input").click()
            themes = list(
                filter(lambda x: x.theme_license == license, self.themes)
            )
            results_table_div = self.driver.find_element(By.ID, 'results')
            rows = BeautifulSoup(results_table_div.get_attribute(
                'innerHTML'), features='lxml').find('table').findAll('tr')

            for i, row in enumerate(rows[1:]):
                tds = row.findAll('td')
                tds_txt = [x.text for x in tds]

                self.assertEqual(
                    tds_txt,
                    [
                        themes[i].cname,
                        themes[i].commit_date[0:10],
                        str(themes[i].stargazers_count),
                        themes[i].commit_sha[0:6],
                        themes[i].theme_license,
                    ],
                )
            self.driver.find_element(
                By.ID, f"{license}-license-selection-input").click()
