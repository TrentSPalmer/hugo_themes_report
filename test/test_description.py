from test.test_selenium import TestSelenium
from unittest import TestCase


class TestDescription(TestSelenium, TestCase):
    def setUp(self):
        super(TestDescription, self).setUp()
        self.plus_button = self.driver.find_element_by_id('plus-button')
        self.desc = self.driver.find_element_by_id('description')
        self.tp_ShowingColumns = "ShowingColumns: "
        self.tp_SortedBy = "; SortedBy: "
        self.tp_Minver = "; FilteredBy: MinHugoVersion="
        self.tp_Licenses = "; Licenses="
        self.tp_Tags = "; Tags="
        self.tp_Features = "; Features="
        self.columns = "theme, date, stars, commit"
        self.sorted_by = "date, stars, name, minVer, license"
        self.min_ver, self.licenses = "none", "none"
        self.tags, self.features = "none", "none"
        self.plus_button.click()

    def coalesced_text_test(self):
        self.assertEqual(
            self.desc.text,
            f"{self.tp_ShowingColumns}{self.columns}"
            f"{self.tp_SortedBy}{self.sorted_by}"
            f"{self.tp_Minver}{self.min_ver}{self.tp_Licenses}{self.licenses}"
            f"{self.tp_Tags}{self.tags}{self.tp_Features}{self.features}")


class TestDefaultDescription(TestDescription, TestCase):
    def test_default_desc(self):
        self.coalesced_text_test()
