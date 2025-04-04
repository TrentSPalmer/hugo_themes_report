from test.test_selenium import TestSelenium
from unittest import TestCase

from selenium.webdriver.common.by import By


class TestScroll(TestSelenium, TestCase):
    def setUp(self):
        super(TestScroll, self).setUp()
        self.plus_button = self.driver.find_element(By.ID, 'plus-button')
        self.minus_button = self.driver.find_element(By.ID, 'minus-button')

    def test_get_scroll_position(self):
        self.assertEqual(
            self.driver.execute_script("return window.pageYOffset"), 0)
        self.driver.execute_script(
            "window.scrollTo(0,document.body.scrollHeight)"
        )
        self.assertGreaterEqual(
            self.driver.execute_script("return window.pageYOffset"), 12061)

    def test_plus_button_scroll_to_top(self):
        self.assertEqual(
            self.driver.execute_script("return window.pageYOffset"), 0)
        self.driver.execute_script(
            "window.scrollTo(0,document.body.scrollHeight)"
        )
        self.assertGreaterEqual(
            self.driver.execute_script("return window.pageYOffset"), 12061)
        self.plus_button.click()
        self.assertEqual(
            self.driver.execute_script("return window.pageYOffset"), 0)

    def test_minus_button_scroll_to_top(self):
        self.plus_button.click()
        self.assertEqual(
            self.driver.execute_script("return window.pageYOffset"), 0)
        self.driver.execute_script(
            "window.scrollTo(0,document.body.scrollHeight)"
        )
        self.assertGreaterEqual(
            self.driver.execute_script("return window.pageYOffset"), 12125)
        self.minus_button.click()
        self.assertEqual(
            self.driver.execute_script("return window.pageYOffset"), 0)
