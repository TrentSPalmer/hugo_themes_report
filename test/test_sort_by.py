from test.test_selenium import TestSelenium
from unittest import TestCase
from test.database import get_themes_as_dicts_of_sortable_columns
from itertools import permutations
from test.theme_compare import theme_compare
from functools import cmp_to_key
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

SBB = [
    'sortByDate',
    'sortByStars',
    'sortByName',
    'sortByMinVer',
    'sortByLicense',
]  # SBB -> sort_by_buttons


class TestsSortBy(TestSelenium, TestCase):
    def setUp(self):
        super(TestsSortBy, self).setUp()
        for x in [
                'plus-button',
                'button-for-showing-columns',
                'commit-column-selection-input',
                'min_ver-column-selection-input',
                'license-column-selection-input',
                'button-for-showing-sort-option',
        ]:
            self.driver.find_element(By.ID, x).click()
        self.themes = get_themes_as_dicts_of_sortable_columns()
        self.tc = len(self.themes)

    def test_sort_by(self):
        for y in permutations(SBB):
            '''
            every time you click a sort_by radio button
            that button moves to the far left
            and then the table rows are re-sorted cumulatively
            '''

            '''
            so first click all the sort_by radio buttons in the
            reverse order of the current permutation
            '''
            for x in y[::-1]:
                self.driver.find_element(By.ID, x).click()

            sort_by_inputs = [x.get_attribute(
                'id') for x in self.driver.find_element(
                By.ID, 'sortByRow').find_elements(By.TAG_NAME, 'input')]
            '''
            and then assert that the sort_by button row is now
            in the same order left->right, as the current
            permutation
            '''
            self.assertEqual(sort_by_inputs, list(y))

            '''
            then sort the list of themes we pulled from the database
            '''
            self.themes.sort(
                key=cmp_to_key(lambda a, b: theme_compare(a, b, y)))

            results_table_div = self.driver.find_element(By.ID, 'results')
            rows = BeautifulSoup(results_table_div.get_attribute(
                'innerHTML'), features='lxml').find('table').findAll('tr')

            '''
            and finally compare the list of themes to the contents of
            the html table in order...PHEW!
            '''
            for i, row in enumerate(rows[1:]):
                tds = row.findAll('td')
                tds_txt = [x.text for x in tds]

                self.assertEqual(
                    tds_txt,
                    [
                        self.themes[i]['name'],
                        self.themes[i]['date'],
                        self.themes[i]['stars'],
                        self.themes[i]['min_ver'],
                        self.themes[i]['license'],
                    ],
                )
