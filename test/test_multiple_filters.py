from test.test_selenium import TestSelenium
from unittest import TestCase
from secrets import choice
from test.database import get_themes_orderedby_cname
from ast import literal_eval
from bs4 import BeautifulSoup
from test.test_filterby_tags import MATCH


class TestMultipleFilters(TestSelenium, TestCase):
    def setUp(self):
        super(TestMultipleFilters, self).setUp()
        for x in [
            'plus-button',
            'button-for-showing-columns',
            'license-column-selection-input',
            'tags-column-selection-input',
            'features-column-selection-input',
            'button-for-showing-sort-option',
            'sortByName',
            'button-for-filter-by-features',
        ]:
            self.driver.find_element_by_id(x).click()
        self.current_filter = 'features'
        self.selected_tags = []
        self.selected_features = []

    def check_content(self):
        self.check_available_feature_labels()
        self.check_available_tag_labels()
        self.check_available_license_labels()
        self.check_table_contents()

    def check_table_contents(self):
        results_table_div = self.driver.find_element_by_id('results')
        rows = BeautifulSoup(results_table_div.get_attribute(
            'innerHTML'), features='lxml').find('table').findAll('tr')

        self.assertEqual(
            len(self.themes), len(rows[1:]), msg=f"{self.themes}\n{rows[1:]}"
        )

        for i, row in enumerate(rows[1:]):
            tds = row.findAll('td')
            tds_txt = [x.text for x in tds]

            self.assertEqual(
                [
                    tds_txt[0],
                    tds_txt[1],
                    tds_txt[2],
                ],
                [
                    self.themes[i].cname,
                    self.themes[i].commit_date[:10],
                    str(self.themes[i].stargazers_count),
                ],
            )

    def check_available_tag_labels(self):
        for button in self.tag_buttons:
            label_text = button.find('label').text
            tag_from_button = MATCH.search(label_text).group(1)
            tc_from_button = int(MATCH.search(label_text).group(2)[2:-1])
            tc_from_selfdotthemes = len([
                x for x in self.themes
                if x.tags_list is not None and tag_from_button
                in literal_eval(x.tags_list)
            ])
            self.assertEqual(
                tc_from_button, tc_from_selfdotthemes, msg=tag_from_button)

    def check_available_license_labels(self):
        for button in self.license_buttons:
            label_text = button.find('label').text
            license_from_button = MATCH.search(label_text).group(1)
            tc_from_button = int(MATCH.search(label_text).group(2)[2:-1])
            tc_from_selfdotthemes = len([
                x for x in self.themes
                if license_from_button == x.theme_license
            ])
            self.assertEqual(tc_from_button, tc_from_selfdotthemes)

    def check_available_feature_labels(self):
        for button in self.feature_buttons:
            label_text = button.find('label').text
            feature_from_button = MATCH.search(label_text).group(1)
            tc_from_button = int(MATCH.search(label_text).group(2)[2:-1])
            tc_from_selfdotthemes = len([
                x for x in self.themes
                if x.features_list is not None and feature_from_button
                in literal_eval(x.features_list)
            ])
            self.assertEqual(
                tc_from_button, tc_from_selfdotthemes, msg=feature_from_button)

    def update_available_licenses(self):
        licenseSelectionRow = self.driver.find_element_by_id(
            'licenseSelectionRow')
        self.license_buttons = BeautifulSoup(
            licenseSelectionRow.get_attribute('innerHTML'), features='lxml'
        ).findAll('button')

    def set_unchecked_features(self):
        featureSelectionRow = self.driver.find_element_by_id(
            'featureSelectionRow')
        inputs = featureSelectionRow.find_elements_by_tag_name('input')
        self.unchecked_features = [
            x.get_attribute('id')[:-24] for x in inputs if not x.is_selected()
        ]
        self.feature_buttons = BeautifulSoup(
            featureSelectionRow.get_attribute('innerHTML'), features='lxml'
        ).findAll('button')

    def set_unchecked_tags(self):
        tagSelectionRow = self.driver.find_element_by_id(
            'tagSelectionRow')
        inputs = tagSelectionRow.find_elements_by_tag_name('input')
        self.unchecked_tags = [
            x.get_attribute('id')[:-20] for x in inputs if not x.is_selected()
        ]
        self.tag_buttons = BeautifulSoup(
            tagSelectionRow.get_attribute('innerHTML'), features='lxml'
        ).findAll('button')

    def update_lists(self):
        self.set_unchecked_features()
        self.set_unchecked_tags()
        self.update_filtered_themes()
        self.update_available_licenses()

    def add_tag_filter(self):
        self.check_random_tag()
        self.check_content()
        if len(self.unchecked_features) > 0:
            self.multiple_filter_test()
        elif len(self.unchecked_tags) > 0:
            self.add_tag_filter()

    def add_feature_filter(self):
        self.check_random_feature()
        self.check_content()
        if len(self.unchecked_tags) > 0:
            self.multiple_filter_test()
        elif len(self.unchecked_features) > 0:
            self.add_feature_filter()

    def check_random_feature(self):
        if len(self.unchecked_features) > 0:
            random_feature = choice(self.unchecked_features[:2])
            self.driver.find_element_by_id(
                f"{random_feature}-feature-selection-input").click()
            self.selected_features.append(random_feature)
            self.update_lists()

    def check_random_tag(self):
        if len(self.unchecked_tags) > 0:
            random_tag = choice(self.unchecked_tags[:2])
            self.driver.find_element_by_id(
                f"{random_tag}-tag-selection-input").click()
            self.selected_tags.append(random_tag)
            self.update_lists()

    def multiple_filter_test(self):
        if self.current_filter == 'tags':
            self.current_filter = 'features'
            self.driver.find_element_by_id(
                'button-for-filter-by-features').click()
            self.add_feature_filter()
        if self.current_filter == 'features':
            self.current_filter = 'tags'
            self.driver.find_element_by_id(
                'button-for-filter-by-tags').click()
            self.add_tag_filter()

    def has_tags_and_features(self, tl, fl):
        if len(self.selected_tags) > 0 and tl is None:
            return False
        elif len(self.selected_features) > 0 and fl is None:
            return False
        else:
            result = True
            if len(self.selected_tags) > 0:
                tags_list = literal_eval(tl)
                for x in self.selected_tags:
                    if x not in tags_list:
                        result = False
            if len(self.selected_features) > 0:
                features_list = literal_eval(fl)
                for y in self.selected_features:
                    if y not in features_list:
                        result = False
            return result

    def update_filtered_themes(self):
        self.themes = [
            x for x in get_themes_orderedby_cname() if
            self.has_tags_and_features(x.tags_list, x.features_list)
        ]

    def test_multiple_filter(self):
        self.update_lists()
        self.multiple_filter_test()
