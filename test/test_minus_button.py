from test.test_selenium import TestSelenium
from unittest import TestCase

from selenium.webdriver.common.by import By


class TestMinusButton(TestSelenium, TestCase):
    def setUp(self):
        super(TestMinusButton, self).setUp()
        self.plus_button = self.driver.find_element(By.ID, 'plus-button')
        self.minus_button = self.driver.find_element(By.ID, 'minus-button')
        self.selection_options_menu = self.driver.find_element(
            By.ID, 'selection-options-menu')

    def test_minus_button_props(self):
        self.assertEqual(
            self.minus_button.value_of_css_property('display'), 'none')
        self.assertEqual(
            self.minus_button.value_of_css_property('height'), '48px')
        self.assertEqual(
            self.minus_button.value_of_css_property('width'), '48px')
        self.assertEqual(
            self.minus_button.value_of_css_property(
                'color'), 'rgba(68, 68, 68, 1)')
        self.assertEqual(
            self.minus_button.value_of_css_property(
                'background-color'), 'rgba(204, 204, 204, 1)')
        self.assertEqual(
            self.selection_options_menu.value_of_css_property(
                'display'), 'none')

    def test_minus_button_after_click_first_level(self):
        self.assertEqual(
            self.plus_button.value_of_css_property('display'), 'block')
        self.plus_button.click()
        self.assertEqual(
            self.minus_button.value_of_css_property('display'), 'block')
        self.minus_button.click()
        self.assertEqual(
            self.minus_button.value_of_css_property('display'), 'none')
        self.assertEqual(
            self.plus_button.value_of_css_property('display'), 'block')
        self.assertEqual(
            self.selection_options_menu.value_of_css_property(
                'display'), 'none')

    def test_minus_button_before_click_first_level(self):
        self.assertEqual(
            self.selection_options_menu.value_of_css_property(
                'display'), 'none')
        self.plus_button.click()
        self.assertEqual(
            self.selection_options_menu.value_of_css_property(
                'display'), 'flex')
