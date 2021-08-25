from test.test_selenium import TestSelenium
from unittest import TestCase
from bs4 import BeautifulSoup as Bs
from test.database import get_themes_orderedby_cname
from ast import literal_eval


class TestShowingColumns(TestSelenium, TestCase):
    def setUp(self):
        super(TestShowingColumns, self).setUp()
        self.driver.find_element_by_id('plus-button').click()
        self.driver.find_element_by_id(
            'button-for-showing-sort-option').click()
        self.driver.find_element_by_id('sortByName').click()
        self.driver.find_element_by_id(
            'button-for-showing-columns').click()
        self.themes = get_themes_orderedby_cname()
        self.tc = len(self.themes)

    def test_non_default_table(self):
        self.driver.find_element_by_id(
            'min_ver-column-selection-input').click()
        self.driver.find_element_by_id(
            'license-column-selection-input').click()
        self.driver.find_element_by_id(
            'desc-column-selection-input').click()
        self.driver.find_element_by_id(
            'tags-column-selection-input').click()
        self.driver.find_element_by_id(
            'features-column-selection-input').click()
        self.driver.find_element_by_id(
            'date-column-selection-input').click()
        self.driver.find_element_by_id(
            'num_stars-column-selection-input').click()
        self.driver.find_element_by_id(
            'commit-column-selection-input').click()
        results_table_div = self.driver.find_element_by_id('results')
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

            self.assertEqual(
                tds_txt,
                [self.themes[i].cname, min_ver, license, desc, tags, features],
            )

    def test_default_table(self):
        results_table_div = self.driver.find_element_by_id('results')
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
