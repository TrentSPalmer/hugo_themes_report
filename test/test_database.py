from unittest import TestCase
from test.database import (
    get_newest_update_time, get_newest_update_time_from_gitlab,
    get_themes_from_gitlab_table_by_date, get_gitlab_themes,
    get_themes, get_themes_from_gitlab_table
)
import time


class TestDataBase(TestCase):
    def test_newest_commit_time(self):
        newest = get_newest_update_time()
        current_time = int(time.time())
        # print(current_time, newest[0], (current_time - newest[0]))
        self.assertTrue((current_time - newest[0]) < 259200)

    def test_newest_commit_time_from_gitlab(self):
        newest = get_newest_update_time_from_gitlab()
        current_time = int(time.time())
        self.assertTrue((current_time - newest[0]) < 864000)

    def test_duplicates(self):
        t_list = get_themes()
        t_list_names = [x.name for x in t_list]
        t_list_shas = [x.commit_sha for x in t_list]
        for x in t_list:
            self.assertEqual(t_list_names.count(x.name), 1)
            self.assertEqual(t_list_shas.count(x.commit_sha), 1)


class TestGitLabData(TestCase):
    def test_duplicates_gitlab_data(self):
        t_list = get_themes_from_gitlab_table()
        t_list_names = [x.name for x in t_list]
        t_list_shas = [x.commit_sha for x in t_list]
        for x in t_list:
            self.assertEqual(t_list_names.count(x.name), 1)
            self.assertEqual(t_list_shas.count(x.commit_sha), 1)

    def test_gitlab_data(self):
        glt_list = get_themes_from_gitlab_table_by_date()
        list_glt = get_gitlab_themes()
        self.assertEqual(len(list_glt), len(glt_list))

        for i, x in enumerate(glt_list):
            self.assertEqual(x.name, list_glt[i].name)
            self.assertEqual(x.url, list_glt[i].url)
            self.assertEqual(x.commit_sha, list_glt[i].commit_sha)
            self.assertEqual(x.commit_date, list_glt[i].commit_date)
            self.assertEqual(
                x.commit_date_in_seconds,
                list_glt[i].commit_date_in_seconds)
            self.assertEqual(
                x.star_count, list_glt[i].stargazers_count)
            self.assertEqual(
                x.themes_toml_content,
                list_glt[i].themes_toml_content)
