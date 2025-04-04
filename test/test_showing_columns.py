import re
from ast import literal_eval
from test.database import get_themes_orderedby_cname
from test.test_selenium import TestSelenium
from unittest import TestCase

from bs4 import BeautifulSoup as Bs
from selenium.webdriver.common.by import By


class TestShowingColumns(TestSelenium, TestCase):
    def setUp(self):
        super(TestShowingColumns, self).setUp()
        self.driver.find_element(By.ID, 'plus-button').click()
        self.driver.find_element(
            By.ID, 'button-for-showing-sort-option').click()
        self.driver.find_element(By.ID, 'sortByName').click()
        self.driver.find_element(
            By.ID, 'button-for-showing-columns').click()
        self.themes = get_themes_orderedby_cname()
        self.tc = len(self.themes)

    def test_non_default_table(self):
        self.driver.find_element(
            By.ID, 'min_ver-column-selection-input').click()
        self.driver.find_element(
            By.ID, 'license-column-selection-input').click()
        self.driver.find_element(
            By.ID, 'desc-column-selection-input').click()
        self.driver.find_element(
            By.ID, 'tags-column-selection-input').click()
        self.driver.find_element(
            By.ID, 'features-column-selection-input').click()
        self.driver.find_element(
            By.ID, 'date-column-selection-input').click()
        self.driver.find_element(
            By.ID, 'num_stars-column-selection-input').click()
        self.driver.find_element(
            By.ID, 'commit-column-selection-input').click()
        results_table_div = self.driver.find_element(By.ID, 'results')
        rows = Bs(results_table_div.get_attribute(
            'innerHTML'), features='lxml').find('table').findAll('tr')

        headings = rows[0].findAll('th')
        headings_txt = [x.text for x in headings]
        self.assertEqual(
            headings_txt,
            [
                f'{self.tc}/{self.tc} themes', 'minVer', 'license',
                'desc', 'tags', 'features',
            ],
        )

        for i, row in enumerate(rows[1:]):
            tds = row.findAll('td')
            tds_txt = [x.text for x in tds]
            tags = '' if self.themes[
                i].tags_list is None else ','.join(
                literal_eval(self.themes[i].tags_list))

            features = '' if self.themes[
                i].features_list is None else ','.join(
                literal_eval(self.themes[i].features_list))

            min_ver = '' if self.themes[
                i].min_ver is None else self.themes[i].min_ver

            license = '' if self.themes[
                i].theme_license is None else self.themes[i].theme_license

            desc = '' if self.themes[i].desc is None else self.themes[i].desc

            if self.themes[i].cname == "Agnes":
                # remove closing html tag in desc
                desc = re.sub(r'</.*>', '', desc)
                # remove opening html tag in desc
                desc = re.sub(r'<.*>', '', desc)

            self.assertEqual(
                tds_txt,
                [self.themes[i].cname, min_ver, license, desc, tags, features],
            )

    def test_default_table(self):
        results_table_div = self.driver.find_element(By.ID, 'results')
        rows = Bs(results_table_div.get_attribute(
            'innerHTML'), features='lxml').find('table').findAll('tr')

        self.assertEqual(len(rows), self.tc + 1)

        headings = rows[0].findAll('th')
        headings_txt = [x.text for x in headings]
        self.assertEqual(
            headings_txt,
            [f'{self.tc}/{self.tc} themes', 'date', 'stars', 'commit'],
        )

        for i, row in enumerate(rows[1:]):
            tds = row.findAll('td')
            tds_txt = [x.text for x in tds]
            self.assertEqual(
                tds_txt,
                [
                    self.themes[i].cname,
                    self.themes[i].commit_date[0:10],
                    str(self.themes[i].stargazers_count),
                    self.themes[i].commit_sha[0:6],
                ],
            )
