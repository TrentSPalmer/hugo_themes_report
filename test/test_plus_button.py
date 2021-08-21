from test.test_selenium import TestSelenium
from unittest import TestCase


class TestPlusButton(TestSelenium, TestCase):
    def setUp(self):
        super(TestPlusButton, self).setUp()
        self.plus_button = self.driver.find_element_by_id('plus-button')
        self.minus_button = self.driver.find_element_by_id('minus-button')
        self.selection_options_menu = self.driver.find_element_by_id(
            'selection-options-menu')

    def test_plus_button_props(self):
        self.assertEqual(
            self.plus_button.value_of_css_property('display'), 'block')
        self.assertEqual(
            self.plus_button.value_of_css_property('height'), '48px')
        self.assertEqual(
            self.plus_button.value_of_css_property('width'), '48px')
        self.assertEqual(
            self.plus_button.value_of_css_property(
                'color'), 'rgba(68, 68, 68, 1)')
        self.assertEqual(
            self.plus_button.value_of_css_property(
                'background-color'), 'rgba(204, 204, 204, 1)')
        self.assertEqual(
            self.selection_options_menu.value_of_css_property(
                'display'), 'none')

    def test_plus_button_before_click(self):
        self.assertEqual(
            self.selection_options_menu.value_of_css_property(
                'display'), 'none')
        self.assertEqual(
            self.minus_button.value_of_css_property('display'), 'none')
        self.assertEqual(
            self.plus_button.value_of_css_property('display'), 'block')

    def test_plus_button_click(self):
        self.plus_button.click()
        self.assertEqual(
            self.plus_button.value_of_css_property('display'), 'none')
        self.assertEqual(
            self.minus_button.value_of_css_property('display'), 'block')
        self.assertEqual(
            self.selection_options_menu.value_of_css_property(
                'display'), 'flex')
