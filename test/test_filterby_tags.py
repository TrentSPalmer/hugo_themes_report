from test.test_selenium import TestSelenium
from unittest import TestCase
from test.database import get_themes_orderedby_cname
from ast import literal_eval
from bs4 import BeautifulSoup
import re
MATCH = re.compile(r'^(.*)(\s\(\d*\))$')


class TestFilterByTags(TestSelenium, TestCase):
    def setUp(self):
        super(TestFilterByTags, self).setUp()
        for x in [
                'plus-button',
                'button-for-showing-columns',
                'tags-column-selection-input',
                'button-for-showing-sort-option',
                'sortByName',
                'button-for-filter-by-tags',
        ]:
            self.driver.find_element_by_id(x).click()
        self.themes = get_themes_orderedby_cname()

    def test_filter_by_tags(self):
        filterby_tags_inputs = self.get_filter_by_tags_inputs()

        for tag in filterby_tags_inputs:
            self.driver.find_element_by_id(
                f"{tag}-tag-selection-input").click()

            themes = [x for x in self.themes if
                      x.tags_list is not None and tag
                      in literal_eval(x.tags_list)]
            self.update_tags_available(themes)

            tagSelectionRow = self.driver.find_element_by_id('tagSelectionRow')
            buttons = BeautifulSoup(
                tagSelectionRow.get_attribute(
                    'innerHTML'), features='lxml').findAll('button')

            self.assertEqual(len(buttons), len(self.tags_available))

            for button in buttons:
                label_text = button.find('label').text
                button_tag = MATCH.search(label_text).group(1)
                button_theme_count = int(MATCH.search(
                    label_text).group(2)[2:-1])
                self.assertEqual(
                    button_theme_count,
                    self.tags_available[button_tag]['num_themes']
                )

            results_table_div = self.driver.find_element_by_id('results')
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
                        themes[i].cname,
                        themes[i].commit_date[0:10],
                        str(themes[i].stargazers_count),
                        themes[i].commit_sha[0:6],
                        set(','.join(literal_eval(themes[i].tags_list))),
                    ],
                )

            self.driver.find_element_by_id(
                f"{tag}-tag-selection-input").click()

    def get_filter_by_tags_inputs(self):
        div = self.driver.find_element_by_id('tagSelectionRow')
        return [x.get_attribute('id')[:-20]
                for x in div.find_elements_by_tag_name('input')]

    def update_tags_available(self, themes):
        self.tags_available = {}
        for theme in themes:
            for tag in literal_eval(theme.tags_list):
                if tag not in self.tags_available:
                    self.tags_available[tag] = {'num_themes': 1}
                else:
                    self.tags_available[tag]['num_themes'] += 1
