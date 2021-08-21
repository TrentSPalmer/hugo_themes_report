from test.test_selenium import TestSelenium
from unittest import TestCase


class TestScroll(TestSelenium, TestCase):
    def setUp(self):
        super(TestScroll, self).setUp()
        self.plus_button = self.driver.find_element_by_id('plus-button')
        self.minus_button = self.driver.find_element_by_id('minus-button')

    def test_get_scroll_position(self):
        self.assertEqual(
            self.driver.execute_script("return window.pageYOffset"), 0)
        self.driver.execute_script(
            "window.scrollTo(0,document.body.scrollHeight)"
        )
        self.assertEqual(
            self.driver.execute_script("return window.pageYOffset"), 12461)

    def test_plus_button_scroll_to_top(self):
        self.assertEqual(
            self.driver.execute_script("return window.pageYOffset"), 0)
        self.driver.execute_script(
            "window.scrollTo(0,document.body.scrollHeight)"
        )
        self.assertEqual(
            self.driver.execute_script("return window.pageYOffset"), 12461)
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
        self.assertEqual(
            self.driver.execute_script("return window.pageYOffset"), 12573)
        self.minus_button.click()
        self.assertEqual(
            self.driver.execute_script("return window.pageYOffset"), 0)
