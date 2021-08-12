#!/usr/bin/env python3
# rank_hugo_themes.py

from jinja2 import Environment, FileSystemLoader
import re
import toml
from calendar import timegm
from time import strptime
from requests import get
# from json import loads as json_loads
from sys import argv as sys_argv
from base64 import b64decode
from ast import literal_eval

from sqlalchemy import create_engine, Column, Integer, VARCHAR, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import deferred, sessionmaker

engine = create_engine('sqlite:///hugothemes.db', echo=False)
Base = declarative_base()
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
template = env.get_template('base.html')


class Tags(Base):
    __tablename__ = 'tags'

    tag = Column(VARCHAR, primary_key=True)
    theme_list = Column(TEXT)
    num_themes = Column(Integer)

    def __repr__(self):
        repr_string = "<(tag = '%s', theme_list = '%s', num_themes = '%s')>"
        repr_values = (self.tag, self.theme_list, self.num_themes)
        return repr_string % repr_values


class Hugothemes_from_gitlab(Base):
    __tablename__ = 'hugothemes_from_gitlab'

    name = Column(VARCHAR, primary_key=True)
    url = Column(TEXT)
    commit_sha = Column(TEXT)
    gitlab_id = Column(TEXT)
    commit_date_in_seconds = Column(Integer)
    commit_date = Column(TEXT)
    star_count = Column(Integer)
    themes_toml_content = Column(TEXT)
    default_branch = Column(TEXT)

    def __repr__(self):
        repr_string = "<(name = '%s', url = '%s', commit_sha = '%s', gitlab_id = '%s', commit_date_in_seconds = '%s'"
        repr_string += ", commit_date = '%s', star_count = '%s', themes_toml_content = '%s', default_branch = '%s')>"
        repr_values = (
            self.name, self.commit_sha, self.gitlab_id,
            self.commit_date_in_seconds, self.commit_date,
            self.star_count, self.themes_toml_content, self.default_branch
        )
        return repr_string % repr_values


class Hugothemes(Base):
    __tablename__ = 'hugothemes'

    name = Column(VARCHAR, primary_key=True)
    ETag = Column(TEXT)
    url = Column(TEXT)
    commit_sha = Column(TEXT)
    commit_date = Column(TEXT)
    commit_date_in_seconds = Column(Integer)
    repo_ETag = Column(TEXT)
    stargazers_count = Column(Integer)
    themes_toml_ETag = Column(TEXT)
    themes_toml_content = deferred(Column(TEXT))
    tags_list = Column(TEXT)
    num_tags = Column(Integer)
    default_branch = Column(TEXT)
    features_list = Column(TEXT)
    num_features = Column(Integer)

    def __repr__(self):
        repr_string = "<(name = '%s', ETag = '%s', url = '%s', commit_sha = '%s', commit_date = '%s'"
        repr_string += ", commit_date_in_seconds = '%s', repo_ETag = '%s', stargazers_count = '%s', themes_toml_ETag = '%s'"
        repr_string += ", themes_toml_content = '%s', tags_list = '%s', num_tags = '%s', default_branch = '%s', features_list = '%s', num_features = '%s')>"
        repr_values = (
            self.name, self.ETag, self.url,
            self.commit_sha, self.commit_date, self.commit_date_in_seconds,
            self.repo_ETag, self.stargazers_count, self.themes_toml_ETag,
            self.themes_toml_content, self.tags_list,
            self.num_tags, self.default_branch, self.features_list, self.num_features,
        )
        return repr_string % repr_values


OLDTHEMESLISTREPO = 'gohugoio/hugoThemes'
THEMESLISTREPO = 'gohugoio/hugoThemesSiteBuilder'
THEMESLIST = []


def get_themes_name_list():
    return [x[11:] for x in THEMESLIST]


def get_gitlab_themes_list():
    return [x for x in THEMESLIST if x[0:10] == 'gitlab.com']


def get_gitlab_themes_name_list():
    return [x[11:] for x in THEMESLIST if x[0:10] == 'gitlab.com']


def get_github_themes_name_list():
    return [x[11:] for x in THEMESLIST if x[0:10] == 'github.com']


if len(sys_argv) == 2:
    headers = {'Authorization': 'token ' + sys_argv[1]}
else:
    headers = {}


def get_hugo_themes_list():
    themes_list_url = f"https://raw.githubusercontent.com/{THEMESLISTREPO}/main/themes.txt"
    response = get(themes_list_url)

    if response.status_code == 200:
        for x in response.text.splitlines():
            if (x[0:10] == 'gitlab.com' or x[0:10] == 'github.com'):
                THEMESLIST.append(x)

    print(response.status_code, get_hugo_themes_list.__name__)


def clean_up():
    themes_name_list = get_themes_name_list()
    session = sessionmaker(bind=engine)()
    hugo_themes_name_list = [theme[0] for theme in session.query(Hugothemes.name).all()]
    for theme_name in hugo_themes_name_list:
        if theme_name not in themes_name_list:
            removed_theme = session.query(Hugothemes).filter_by(name=theme_name).first()
            session.delete(removed_theme)
            session.commit()

    gitlab_themes_name_list = get_gitlab_themes_name_list()
    hugo_themes_from_gitlab_name_list = [theme[0] for theme in session.query(Hugothemes_from_gitlab.name).all()]
    for theme in hugo_themes_from_gitlab_name_list:
        if theme not in gitlab_themes_name_list:
            removed_theme = session.query(Hugothemes_from_gitlab).filter_by(name=theme).first()
            session.delete(removed_theme)
            session.commit()


def parse_gitlab_hugo_themes_list():
    session = sessionmaker(bind=engine)()
    gitlab_themes_list = get_gitlab_themes_list()
    for theme in gitlab_themes_list:
        theme_name = theme[11:]
        existing_theme = session.query(Hugothemes_from_gitlab).filter_by(name=theme_name).first()
        if existing_theme is None:
            session.add(Hugothemes_from_gitlab(name=theme_name, url=theme))
            session.commit()
        else:
            if existing_theme.url != theme:
                existing_theme.url = theme
                session.commit()


def parse_hugo_themes_list():
    session = sessionmaker(bind=engine)()
    for theme in THEMESLIST:
        theme_name = theme[11:]
        existing_theme = session.query(Hugothemes).filter_by(name=theme_name).first()
        if existing_theme is None:
            session.add(Hugothemes(name=theme_name, url=theme))
            session.commit()
        else:
            if existing_theme.url != theme:
                existing_theme.url = theme
                session.commit()


def get_gitlab_project_ids():
    session = sessionmaker(bind=engine)()
    themes = (theme[0] for theme in session.query(Hugothemes_from_gitlab.name).all())
    match = re.compile(r'(Project ID: )(\d{5,})')
    for theme in themes:
        gitlab_theme = session.query(Hugothemes_from_gitlab).filter_by(name=theme).one()
        if gitlab_theme.gitlab_id is None:
            response = get(f"https://{gitlab_theme.url}")
            if response.status_code == 200:
                gitlab_theme.gitlab_id = match.search(response.text).group(2)
                session.commit()
            if response.status_code == 404:
                print(response.status_code, get_gitlab_project_ids.__name__, theme)
            print(response.status_code, get_gitlab_project_ids.__name__)


def get_commit_info_for_hugo_themes():
    session = sessionmaker(bind=engine)()
    theme_names_from_github = get_github_themes_name_list()
    for hugo_theme in theme_names_from_github:
        theme = session.query(Hugothemes).filter_by(name=hugo_theme).one()
        api_call_url = f'https://api.github.com/repos/{theme.name}/commits/{theme.default_branch}'

        if theme.ETag is not None:
            headers['If-None-Match'] = theme.ETag
        else:
            if 'If-None-Match' in headers:
                del headers['If-None-Match']

        if len(headers) == 0:
            response = get(api_call_url)
        else:
            response = get(api_call_url, headers=headers)
        if response.status_code == 422:
            print(hugo_theme)
            quit()
        if response.status_code == 200:
            theme.ETag = response.headers['ETag'].lstrip('W/')
            result = response.json()
            theme.commit_date = result['commit']['author']['date']
            theme.commit_date_in_seconds = timegm(strptime(theme.commit_date, '%Y-%m-%dT%H:%M:%SZ'))
            theme.commit_sha = result['commit']['tree']['sha']
            session.commit()
        elif response.status_code == 403:
            print(response.status_code, get_commit_info_for_hugo_themes.__name__)
            # write_reports()
            quit()
        elif response.status_code == 404:
            print(response.status_code, get_commit_info_for_hugo_themes.__name__, hugo_theme)
        print(response.status_code, get_commit_info_for_hugo_themes.__name__)


def get_commit_info_for_hugo_themes_from_gitlab():
    session = sessionmaker(bind=engine)()
    theme_names_from_gitlab = get_gitlab_themes_name_list()
    # match = re.compile(r'(\.\d{3})(Z$)')
    for hugo_theme in theme_names_from_gitlab:
        theme = session.query(Hugothemes_from_gitlab).filter_by(name=hugo_theme).one()
        api_call_url = f'https://gitlab.com/api/v4/projects/{theme.gitlab_id}/repository/commits/{theme.default_branch}'

        response = get(api_call_url)
        if response.status_code == 200:
            result = response.json()
            # theme.commit_date = (match.sub(r'\2', result['created_at']))[0:19] + 'Z'
            theme.commit_date = result['created_at'][0:19] + 'Z'
            theme.commit_date_in_seconds = timegm(strptime(theme.commit_date, '%Y-%m-%dT%H:%M:%SZ'))
            theme.commit_sha = result['id']
            session.commit()
        elif response.status_code == 403:
            print(response.status_code, get_commit_info_for_hugo_themes_from_gitlab.__name__)
            # write_reports()
            quit()
        elif response.status_code == 404:
            print(response.status_code, get_commit_info_for_hugo_themes_from_gitlab.__name__, hugo_theme)
        print(response.status_code, get_commit_info_for_hugo_themes_from_gitlab.__name__)


def get_stargazer_count_for_hugo_themes():
    session = sessionmaker(bind=engine)()
    theme_names_from_github = get_github_themes_name_list()
    for hugo_theme in theme_names_from_github:
        theme = session.query(Hugothemes).filter_by(name=hugo_theme).one()
        api_call_url = 'https://api.github.com/repos/' + theme.name

        if theme.repo_ETag is not None:
            headers['If-None-Match'] = theme.repo_ETag
        else:
            if 'If-None-Match' in headers:
                del headers['If-None-Match']

        if len(headers) == 0:
            response = get(api_call_url)
        else:
            response = get(api_call_url, headers=headers)
        if response.status_code == 200:
            theme.repo_ETag = response.headers['ETag'].lstrip('W/')
            result = response.json()
            theme.stargazers_count = result['stargazers_count']
            theme.default_branch = result['default_branch']
            session.commit()
        elif response.status_code == 403:
            print(response.status_code, get_stargazer_count_for_hugo_themes.__name__)
            # write_reports()
            quit()
        elif response.status_code == 404:
            print(response.status_code, get_stargazer_count_for_hugo_themes.__name__, hugo_theme)
        print(response.status_code, get_stargazer_count_for_hugo_themes.__name__)


def get_stargazer_count_for_hugo_themes_from_gitlab():
    session = sessionmaker(bind=engine)()
    theme_names_from_gitlab = get_gitlab_themes_name_list()
    for hugo_theme in theme_names_from_gitlab:
        theme = session.query(Hugothemes_from_gitlab).filter_by(name=hugo_theme).one()
        api_call_url = f'https://gitlab.com/api/v4/projects/{theme.gitlab_id}'
        response = get(api_call_url)
        if response.status_code == 200:
            result = response.json()
            if theme.star_count != result['star_count']:
                theme.star_count = result['star_count']
            if theme.default_branch != result['default_branch']:
                theme.default_branch = result['default_branch']
            session.commit()
        elif response.status_code == 403:
            print(response.status_code, get_stargazer_count_for_hugo_themes_from_gitlab.__name__)
            # write_reports()
            quit()
        elif response.status_code == 404:
            print(response.status_code, get_stargazer_count_for_hugo_themes_from_gitlab.__name__, hugo_theme)
        print(response.status_code, get_stargazer_count_for_hugo_themes_from_gitlab.__name__)


def get_theme_dot_toml_for_each_hugo_themes():
    session = sessionmaker(bind=engine)()
    theme_names_from_github = get_github_themes_name_list()
    for hugo_theme in theme_names_from_github:
        theme = session.query(Hugothemes).filter_by(name=hugo_theme).one()
        if theme.name == 'gcushen/hugo-academic':
            theme_toml = 'wowchemy/theme.toml'
        else:
            theme_toml = 'theme.toml'
        api_call_url = f"https://api.github.com/repos/{theme.name}/contents/{theme_toml}"

        if theme.themes_toml_ETag is not None:
            headers['If-None-Match'] = theme.themes_toml_ETag
        else:
            if 'If-None-Match' in headers:
                del headers['If-None-Match']

        if len(headers) == 0:
            response = get(api_call_url)
        else:
            response = get(api_call_url, headers=headers)
        if response.status_code == 200:
            theme.themes_toml_ETag = response.headers['ETag'].lstrip('W/')
            result = response.json()
            theme.themes_toml_content = result['content']
            session.commit()
        elif response.status_code == 403:
            print(response.status_code, get_theme_dot_toml_for_each_hugo_themes.__name__)
            # write_reports()
            quit()
        elif response.status_code == 404:
            print(response.status_code, get_theme_dot_toml_for_each_hugo_themes.__name__, hugo_theme)
        print(response.status_code, get_theme_dot_toml_for_each_hugo_themes.__name__)


def get_theme_dot_toml_for_each_hugo_themes_from_gitlab():
    session = sessionmaker(bind=engine)()
    theme_names_from_gitlab = get_gitlab_themes_name_list()
    for hugo_theme in theme_names_from_gitlab:
        theme = session.query(Hugothemes_from_gitlab).filter_by(name=hugo_theme).one()
        api_call_url = f'https://gitlab.com/api/v4/projects/{theme.gitlab_id}/repository/files/theme.toml?ref={theme.default_branch}'
        response = get(api_call_url)
        if response.status_code == 200:
            result = response.json()
            theme.themes_toml_content = result['content']
            session.commit()
        elif response.status_code == 403:
            print(response.status_code, get_theme_dot_toml_for_each_hugo_themes_from_gitlab.__name__)
            # write_reports()
            quit()
        elif response.status_code == 404:
            print(response.status_code, get_theme_dot_toml_for_each_hugo_themes_from_gitlab.__name__, hugo_theme)
        print(response.status_code, get_theme_dot_toml_for_each_hugo_themes_from_gitlab.__name__)


def coalesce_themes():
    session = sessionmaker(bind=engine)()
    theme_names_from_gitlab = get_gitlab_themes_name_list()
    for hugo_theme in theme_names_from_gitlab:
        htfgitlab = session.query(Hugothemes_from_gitlab).filter_by(name=hugo_theme).one()
        theme = session.query(Hugothemes).filter_by(name=hugo_theme).first()
        if theme is None:
            session.add(Hugothemes(
                name=hugo_theme, url=htfgitlab.url, commit_sha=htfgitlab.commit_sha,
                commit_date=htfgitlab.commit_date, commit_date_in_seconds=htfgitlab.commit_date_in_seconds,
                stargazers_count=htfgitlab.star_count, themes_toml_content=htfgitlab.themes_toml_content
            ))
        else:
            if theme.url != htfgitlab.url: theme.url = htfgitlab.url
            if theme.commit_sha != htfgitlab.commit_sha: theme.commit_sha = htfgitlab.commit_sha
            if theme.commit_date != htfgitlab.commit_date: theme.commit_date = htfgitlab.commit_date
            if theme.commit_date_in_seconds != htfgitlab.commit_date_in_seconds:
                theme.commit_date_in_seconds = htfgitlab.commit_date_in_seconds
            if theme.stargazers_count != htfgitlab.star_count: theme.stargazers_count = htfgitlab.star_count
            theme.themes_toml_content = htfgitlab.themes_toml_content
        session.commit()


def update_features_list_for_each_hugo_themes():
    session = sessionmaker(bind=engine)()
    themes = [theme[0] for theme in session.query(Hugothemes.name).all()]
    match = re.compile(r'\s(\d+\.\d+\.\d+)\s')
    for hugo_theme in themes:
        theme = session.query(Hugothemes).filter_by(name=hugo_theme).one()
        if theme.themes_toml_content is not None:
            content = b64decode(theme.themes_toml_content).decode('utf-8')
            theme_toml = toml.loads(match.sub(r'"\1"\n', content))
            if 'features' in theme_toml:
                if len(theme_toml['features']) > 0:
                    theme_features = [feature.lower() for feature in theme_toml['features'] if len(feature) > 1]
                    if theme.num_features != len(theme_features): theme.num_features = len(theme_features)
                    if theme.num_features > 0:
                        if theme.features_list != str(theme_features): theme.features_list = str(theme_features)
                    else:
                        if theme.features_list is not None: theme.features_list = None
                else:
                    if theme.features_list is not None: theme.features_list = None
                    if theme.num_features != 0: theme.num_features = 0
            else:
                if theme.features_list is not None: theme.features_list = None
                if theme.num_features != 0: theme.num_features = 0
        else:
            if theme.features_list is not None: theme.features_list = None
            if theme.num_features != 0: theme.num_features = 0
        session.commit()


def get_corrected_tags(tags):
    result = []
    correct = True
    for tag in tags:
        if (len(tag) > 50): correct = False
    if not correct:
        for tag in tags:
            result += [x.lstrip() for x in tag.split(',')]
        return result
    else:
        return tags


def update_tags_list_for_each_hugo_themes():
    session = sessionmaker(bind=engine)()
    themes = [theme[0] for theme in session.query(Hugothemes.name).all()]
    match = re.compile(r'\s(\d+\.\d+\.\d+)\s')
    for hugo_theme in themes:
        theme = session.query(Hugothemes).filter_by(name=hugo_theme).one()
        if theme.themes_toml_content is not None:
            content = b64decode(theme.themes_toml_content).decode('utf-8')
            # put quotes around any unquoted double-dotted version numbers
            # (and add a newline afterwards)
            # because python toml libraries will error out on those
            theme_toml = toml.loads(match.sub(r'"\1"\n', content))
            if 'tags' in theme_toml:
                if len(theme_toml['tags']) > 0:
                    corrected_tags = get_corrected_tags(theme_toml['tags'])
                    theme_tags = [tag.lower() for tag in corrected_tags if len(tag) > 1]
                    if theme.num_tags != len(theme_tags): theme.num_tags = len(theme_tags)
                    if theme.num_tags > 0:
                        if theme.tags_list != str(theme_tags): theme.tags_list = str(theme_tags)
                    else:
                        if theme.tags_list is not None: theme.tags_list = None
                else:
                    if theme.tags_list is not None: theme.tags_list = None
                    if theme.num_tags != 0: theme.num_tags = 0
            else:
                if theme.tags_list is not None: theme.tags_list = None
                if theme.num_tags != 0: theme.num_tags = 0
        else:
            if theme.tags_list is not None: theme.tags_list = None
            if theme.num_tags != 0: theme.num_tags = 0
        session.commit()


def update_tag_table():
    session = sessionmaker(bind=engine)()
    themes = [(theme, tags_list) for theme, tags_list in session.query(
        Hugothemes.name, Hugothemes.tags_list).filter(Hugothemes.name != THEMESLISTREPO).all()]
    tags_list = set()
    for theme in themes:
        if theme[1] is not None:
            tags = literal_eval(theme[1])
            for tag in tags:
                if len(tag) > 0:
                    tags_list.add(tag)

    for hugo_tag in tags_list:
        theme_list = []
        for theme in themes:
            if theme[1] is not None:
                tags = literal_eval(theme[1])
                if hugo_tag in tags:
                    theme_list.append(theme[0])
        tag = session.query(Tags).filter_by(tag=hugo_tag).first()
        if tag is None:
            session.add(Tags(tag=hugo_tag, theme_list=str(theme_list), num_themes=len(theme_list)))
        else:
            theme_list, num_themes = str(theme_list), len(theme_list)
            if tag.theme_list != theme_list: tag.theme_list = theme_list
            if tag.num_themes != num_themes: tag.num_themes = num_themes
    session.commit()


def make_buttons(tags_list):
    button_block = "\t\t<div id='all-tags' class='d-flex flex-wrap justify-content-around'>\n"
    for tag in tags_list:
        button_block += "\t\t\t<div class='d-flex'><a href='#" + tag[0] + "-by-date'><button type='button' class='btn btn-outline-primary'>" + tag[0] + ", " + str(tag[2]) + "</button></a></div>\n"
    button_block += "\t\t</div>\n"
    return button_block


def make_nav_buttons(button_info):
    button_block = "\t\t<div id='" + button_info[0] + "-" + button_info[1] + "' class='d-flex flex-wrap justify-content-around'>\n"
    button_block += "\t\t\t<div class='d-flex'><a href='#all-tags'><button type='button' class='btn btn-outline-primary'>tags</button></a></div>\n"
    if button_info[2] > 10:
        button_block += "\t\t\t<div class='d-flex'><a href='#" + button_info[0] + "-by-date'><button type='button' class='btn btn-outline-primary'>" + button_info[0] + " by date</button></a></div>\n"
        button_block += "\t\t\t<div class='d-flex'><a href='#" + button_info[0] + "-by-stars'><button type='button' class='btn btn-outline-primary'>" + button_info[0] + " by stars</button></a></div>\n"
    button_block += "\t\t</div>\n"
    return button_block


def make_table(themes_info):
    table = "\t<div class='container'>\n\t\t<table class='table monospace'>\n\t\t\t<thead><tr><th scope='col'>" + themes_info[1] + " (tag) " + themes_info[2] + "</th><th scope='col'>Date</th></tr></thead>\n\t\t\t<tbody>\n"
    for theme in themes_info[0]:
        name = theme[0].split('/')[1]
        row = f"\t\t\t\t<tr><td scope='row'><a target='_blank' href='https://{theme[4]}'>{name}</a></td>"
        row += "<td nowrap>" + theme[2][:10] + "</td>"
        row += "<td align='right' nowrap style='padding-left:1em;'>" + str(theme[3]) + '&#x2605' + "</td>"
        row += "<td align='right' style='padding-left:1em;'>" + theme[1][:6] + "</td></tr>\n"
        table += row
    table += "\t\t\t</tbody>\n\t\t</table>\n\t</div>\n"
    return table


def make_section(section_info):
    if section_info[3] > 10:
        section = make_nav_buttons((section_info[0], 'by-date', section_info[3]))
        section += make_table((section_info[1], section_info[0], 'by-date'))
        section += make_nav_buttons((section_info[0], 'by-stars', section_info[3]))
        section += make_table((section_info[2], section_info[0], 'by-stars'))
    else:
        section = make_nav_buttons((section_info[0], 'by-date', section_info[3]))
        section += make_table((section_info[1], section_info[0], 'by-date'))
    return section


def write_reports():
    session = sessionmaker(bind=engine)()
    u, v, w, x, y, z = Hugothemes.name, Hugothemes.commit_sha, Hugothemes.commit_date, Hugothemes.stargazers_count, Hugothemes.url, Hugothemes.commit_date_in_seconds
    themes_bydate_list = [(vals) for (vals) in session.query(u, v, w, x, y).order_by(z.desc())]
    themes_bystars_list = [(vals) for (vals) in session.query(u, v, w, x, y).order_by(x.desc())]
    themes = [theme[0] for theme in themes_bystars_list]
    tags_list = [('all', str(themes), len(themes))]
    tags_list += [(vals) for (vals) in session.query(Tags.tag, Tags.theme_list, Tags.num_themes).filter(Tags.num_themes > 2).order_by(Tags.num_themes.desc())]

    reportpage = "<!DOCTYPE html>\n<html lang='en'>\n"
    reportpage += "\t<head>\n\t\t<title>Hugo Themes Report</title>\n\t\t<meta charset='utf-8'>"
    reportpage += "\n\t\t<meta name='viewport' content='width=device-width, initial-scale=1'>\n"
    reportpage += "\t\t<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css' "
    reportpage += "integrity='sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm' crossorigin='anonymous'>\n\t</head>\n"
    reportpage += "\t<body>\n"

    reportpage += make_section(('all', themes_bydate_list, themes_bystars_list, len(themes_bydate_list)))
    reportpage += make_buttons(tags_list)
    for tag in tags_list[1:]:
        tag_theme_list = literal_eval(tag[1])
        bydate_list = [theme for theme in themes_bydate_list if theme[0] in tag_theme_list]
        bystars_list = [theme for theme in themes_bystars_list if theme[0] in tag_theme_list]
        reportpage += make_section((tag[0], bydate_list, bystars_list, tag[2]))

    reportpage += "\t</body>"
    reportpage += "\n</html>"
    by_date = open('hugo-themes-report/hugo-themes-report.html', 'w')
    by_date.write(reportpage)
    by_date.close()


def generate_report():
    session = sessionmaker(bind=engine)()
    hugo_themes = [
        {
            'name': theme.name,
            'commit': theme.commit_sha[0:6],
            'date': theme.commit_date[0:10],
            'date_in_seconds': theme.commit_date_in_seconds,
            'url': f'https://{theme.url}',
            'short_name': theme.name.split('/')[1],
            'num_stars': theme.stargazers_count,
            'tags': literal_eval(theme.tags_list) if theme.tags_list is not None else [],
            'features': literal_eval(theme.features_list) if theme.features_list is not None else [],
        } for theme in session.query(Hugothemes).all()
    ]
    output = template.render(themes=hugo_themes)
    index_page = open('hugo-themes-report/hugo-themes-report.html', 'w')
    index_page.write(output)
    index_page.close()


if __name__ == "__main__":
    '''
    update_tags_list_for_each_hugo_themes()
    update_features_list_for_each_hugo_themes()
    generate_report()
    '''
    get_hugo_themes_list()
    if len(THEMESLIST) > 300:
        clean_up()
        parse_hugo_themes_list()
        parse_gitlab_hugo_themes_list()
        get_gitlab_project_ids()
        get_stargazer_count_for_hugo_themes()
        get_stargazer_count_for_hugo_themes_from_gitlab()
        get_commit_info_for_hugo_themes()
        get_commit_info_for_hugo_themes_from_gitlab()
        get_theme_dot_toml_for_each_hugo_themes()
        get_theme_dot_toml_for_each_hugo_themes_from_gitlab()
        coalesce_themes()
        update_tags_list_for_each_hugo_themes()
        update_features_list_for_each_hugo_themes()
        update_tag_table()
        # write_reports()
        generate_report()
