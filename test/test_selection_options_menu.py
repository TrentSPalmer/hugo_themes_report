from test.test_selenium import TestSelenium
from unittest import TestCase

DBI = [
    'button-for-showing-sort-option',
    'button-for-showing-columns',
    'button-for-filter-by-minver',
    'button-for-filter-by-tags',
    'button-for-filter-by-features',
    'button-for-filter-by-license',
    'button-for-filter-by-tags-and-features',
]  # DBI -> default_button_ids

FLEXROWS = [
    'sortByRow',
    'columnSelectionHeadingRow',
    'columnSelectionRow',
    'minVerSelectionHeadingRow',
    'minVerSelectionRow',
    'tagSelectionHeadingRow',
    'tagSelectionRow',
    'featureSelectionHeadingRow',
    'featureSelectionRow',
    'licenseSelectionHeadingRow',
    'licenseSelectionRow',
]


class TestSelectionOptionsMenu(TestSelenium, TestCase):
    def setUp(self):
        super(TestSelectionOptionsMenu, self).setUp()
        self.driver.find_element_by_id('plus-button').click()
        self.div = self.driver.find_element_by_id('selection-options-menu')

    def display_is_d_test(self, y_list, d):
        for x in y_list:
            self.assertEqual(
                self.driver.find_element_by_id(
                    x).value_of_css_property('display'), d)

    def test_default_selection_options_menu_buttons_exist(self):
        self.display_is_d_test(DBI, 'block')
        ids = [x.get_attribute(
            'id') for x in self.div.find_elements_by_tag_name('button')]
        self.assertEqual(ids, DBI)

    def test_buttons(self):
        self.display_is_d_test(DBI, 'block')
        for i, x in enumerate(DBI):
            button = self.driver.find_element_by_id(x)
            button.click()
            self.assertEqual(button.value_of_css_property('display'), 'none')
            self.display_is_d_test([*DBI[0:i], *DBI[i + 1:]], 'block')
            if i == 0:
                self.display_is_d_test([FLEXROWS[0]], 'flex')
                self.display_is_d_test(FLEXROWS[1:], 'none')
            elif i == 1:
                self.display_is_d_test(FLEXROWS[1:3], 'flex')
                self.display_is_d_test([FLEXROWS[0], *FLEXROWS[3:]], 'none')
            elif i == 2:
                self.display_is_d_test(FLEXROWS[3:5], 'flex')
                self.display_is_d_test([*FLEXROWS[0:3], *FLEXROWS[5:]], 'none')
            elif i == 3:
                self.display_is_d_test(FLEXROWS[5:7], 'flex')
                self.display_is_d_test([*FLEXROWS[0:5], *FLEXROWS[7:]], 'none')
            elif i == 4:
                self.display_is_d_test(FLEXROWS[7:9], 'flex')
                self.display_is_d_test([*FLEXROWS[0:7], *FLEXROWS[9:]], 'none')
            elif i == 5:
                self.display_is_d_test(FLEXROWS[9:11], 'flex')
                self.display_is_d_test(FLEXROWS[0:9], 'none')
            else:
                self.display_is_d_test(FLEXROWS[5:9], 'flex')
                self.display_is_d_test([*FLEXROWS[0:5], *FLEXROWS[9:]], 'none')
