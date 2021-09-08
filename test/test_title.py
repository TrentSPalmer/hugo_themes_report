from test.test_selenium import TestSelenium
from unittest import TestCase


class TestTitle(TestSelenium, TestCase):
    def setUp(self):
        super(TestTitle, self).setUp()
        self.x = self.driver.find_elements_by_tag_name('h1')

    def test_title(self):
        self.assertEqual(len(self.x), 1)
        self.assertEqual(self.x[0].get_attribute('id'), 'title')
        self.assertEqual(
            self.x[0].value_of_css_property('text-align'), 'center')
        self.assertEqual(self.x[0].value_of_css_property('display'), 'block')
        self.assertEqual(
            self.x[0].value_of_css_property('max-width'), '1856px')
        self.assertEqual(self.x[0].value_of_css_property('font-size'), '32px')
        self.assertEqual(self.x[0].value_of_css_property('font-weight'), '700')
        self.assertEqual(
            self.x[0].value_of_css_property('font-family'), 'sans-serif')

    def test_title_anchor(self):
        x_anchors = self.x[0].find_elements_by_tag_name('a')
        self.assertEqual(len(x_anchors), 1)
        self.assertEqual(
            x_anchors[0].get_attribute('href'),
            'https://github.com/TrentSPalmer/hugo_themes_report'
        )
        self.assertEqual(x_anchors[0].get_attribute('target'), '_blank')
