from test.database import get_themes_orderedby_cname
from test.test_selenium import TestSelenium
from test.theme_compare import compare_jk, semver_split
from unittest import TestCase
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup


class TestFilterByMinVer(TestSelenium, TestCase):
    def setUp(self):
        super(TestFilterByMinVer, self).setUp()
        for x in [
                'plus-button',
                'button-for-showing-columns',
                'min_ver-column-selection-input',
                'button-for-showing-sort-option',
                'sortByName',
                'button-for-filter-by-minver',
        ]:
            self.driver.find_element(By.ID, x).click()
        self.themes = get_themes_orderedby_cname()

    def test_filter_by_min_ver(self):
        filterby_mv_inputs = [x.get_attribute('id')[0:-33]
                              for x in self.driver.find_element(
            By.ID, 'minVerSelectionRow').find_elements(By.TAG_NAME, 'input')]

        for m_ver in filterby_mv_inputs:
            self.driver.find_element(
                By.ID, f'{m_ver}-select-minver-radio-button-input').click()
            if m_ver == 'none':
                themes = self.themes
            else:
                split_mver = semver_split(m_ver)
                themes = list(
                    filter(
                        lambda x: x.min_ver is not None and compare_jk(
                            split_mver, semver_split(x.min_ver)
                        ) != 1, self.themes
                    )
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
                        '' if themes[i].min_ver is None else themes[i].min_ver,
                    ],
                )
