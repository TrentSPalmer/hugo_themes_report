#!/usr/bin/env python3
# rank_hugo_themes.py

import re
from ast import literal_eval
from base64 import b64decode
from calendar import timegm
from sys import argv as sys_argv
from time import strptime

import toml
import yaml
from jinja2 import Environment, FileSystemLoader
from requests import get
from sqlalchemy import TEXT, VARCHAR, Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import deferred, sessionmaker

engine = create_engine("sqlite:///hugothemes.db", echo=False)
Base = declarative_base()
file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)
template = env.get_template("base.html")


class Hugothemes_from_gitlab(Base):
    __tablename__ = "hugothemes_from_gitlab"

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
        return f"<Hugothemes_from_gitlab(name={self.name})>"


class Hugothemes(Base):
    __tablename__ = "hugothemes"

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
    theme_license = Column(TEXT)
    min_ver = Column(TEXT)
    desc = Column(TEXT)
    cname = Column(TEXT)

    def __repr__(self):
        return f"<Hugothemes(name={self.name})>"


OLDTHEMESLISTREPO = "gohugoio/hugoThemes"
THEMESLISTREPO = "gohugoio/hugoThemesSiteBuilder"
THEMESLIST = []
THEMESYAMLTHEMES = ("AminZibayi/Corporio",)


def get_themes_name_list():
    return [x[11:] for x in THEMESLIST]


def get_gitlab_themes_list():
    return [x for x in THEMESLIST if x[0:10] == "gitlab.com"]


def get_gitlab_themes_name_list():
    return [x[11:] for x in THEMESLIST if x[0:10] == "gitlab.com"]


def get_github_themes_name_list():
    return [x[11:] for x in THEMESLIST if x[0:10] == "github.com"]


if len(sys_argv) == 2:
    headers = {"Authorization": "token " + sys_argv[1]}
else:
    headers = {}


def get_hugo_themes_list():
    themes_list_url = "https://raw.githubusercontent.com/"
    themes_list_url += f"{THEMESLISTREPO}/main/themes.txt"
    response = get(themes_list_url)

    if response.status_code == 200:
        lower_case_themes_list = []
        for x in response.text.splitlines():
            if "wowchemy-hugo-themes" not in x and "hugo-theme-ladder" not in x:
                """
                inventory-hugo-theme,
                alexa-portfolio, hugo-theme-ladder, hermit-V2 malformed themes.toml
                """
                if "HugoBlox" not in x:
                    if "alexa-portfolio" not in x and "hermit-V2" not in x:
                        # if "inventory-hugo-theme" not in x:
                        if x[0:10] == "gitlab.com" or x[0:10] == "github.com":
                            if x.lower() not in lower_case_themes_list:
                                if x[-1] == " " and "termishTheme" in x:
                                    x = x[0:-1]
                                THEMESLIST.append(x)
                                lower_case_themes_list.append(x.lower())

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
    hugo_themes_from_gitlab_name_list = [
        theme[0] for theme in session.query(Hugothemes_from_gitlab.name).all()
    ]
    for theme in hugo_themes_from_gitlab_name_list:
        if theme not in gitlab_themes_name_list:
            removed_theme = (
                session.query(Hugothemes_from_gitlab).filter_by(name=theme).first()
            )
            session.delete(removed_theme)
            session.commit()


def dedup_database():
    session = sessionmaker(bind=engine)()
    hugo_themes_sha_list = [
        theme[0] for theme in session.query(Hugothemes.commit_sha).all()
    ]
    sha_list = [
        sha for sha in hugo_themes_sha_list if hugo_themes_sha_list.count(sha) > 1
    ]
    for sha in sha_list:
        removed_theme = session.query(Hugothemes).filter_by(commit_sha=sha).first()
        session.delete(removed_theme)
        session.commit()

    hugo_themes_sha_list_from_gitlab = [
        theme[0] for theme in session.query(Hugothemes_from_gitlab.commit_sha).all()
    ]
    sha_list_from_gitlab = [
        sha
        for sha in hugo_themes_sha_list_from_gitlab
        if hugo_themes_sha_list_from_gitlab.count(sha) > 1
    ]
    for sha in sha_list_from_gitlab:
        removed_theme = (
            session.query(Hugothemes_from_gitlab).filter_by(commit_sha=sha).first()
        )
        session.delete(removed_theme)
        session.commit()


def parse_gitlab_hugo_themes_list():
    session = sessionmaker(bind=engine)()
    gitlab_themes_list = get_gitlab_themes_list()
    for theme in gitlab_themes_list:
        theme_name = theme[11:]
        existing_theme = (
            session.query(Hugothemes_from_gitlab).filter_by(name=theme_name).first()
        )
        if existing_theme is None:
            session.add(Hugothemes_from_gitlab(name=theme_name, url=theme))
            session.commit()
        else:
            if existing_theme.url != theme:
                existing_theme.url = theme
                session.commit()


def get_corrected_url(x):
    if "blox-tailwind" in x:
        return "github.com/HugoBlox/hugo-blox-builder/tree/main/modules/blox-tailwind"
    return get_vnum_stripped_string(x)


def parse_hugo_themes_list():
    session = sessionmaker(bind=engine)()
    for theme in THEMESLIST:
        theme_name = theme[11:]
        theme_url = get_corrected_url(theme)
        existing_theme = session.query(Hugothemes).filter_by(name=theme_name).first()
        if existing_theme is None:
            session.add(Hugothemes(name=theme_name, url=theme_url))
            session.commit()
        else:
            if existing_theme.url != theme_url:
                existing_theme.url = theme_url
                session.commit()


def get_gitlab_project_ids():
    session = sessionmaker(bind=engine)()
    themes = (theme[0] for theme in session.query(Hugothemes_from_gitlab.name).all())
    # match = re.compile(r"(Project ID: )(\d{5,})")
    # need new regex gitlab moved my cheese
    match = re.compile(r"(Project\/)(\d{8})")
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


def get_corrected_theme_name(x):
    return get_vnum_stripped_string(x)


def get_vnum_stripped_string(x):
    if x[-3:] in ("/v2", "/v3", "/v4", "/v5"):
        return x[0:-3]
    else:
        return x


def get_commit_info_for_hugo_themes():
    session = sessionmaker(bind=engine)()
    theme_names_from_github = get_github_themes_name_list()
    for hugo_theme in theme_names_from_github:
        theme = session.query(Hugothemes).filter_by(name=hugo_theme).one()
        theme_name = get_corrected_theme_name(theme.name)
        api_call_url = "https://api.github.com/repos/"
        if "blox-tailwind" in theme_name:
            api_call_url += "HugoBlox/hugo-blox-builder/commits/main"
        else:
            api_call_url += f"{theme_name}/commits/{theme.default_branch}"

        if theme.ETag is not None:
            headers["If-None-Match"] = theme.ETag
        else:
            if "If-None-Match" in headers:
                del headers["If-None-Match"]

        if len(headers) == 0:
            response = get(api_call_url)
        else:
            response = get(api_call_url, headers=headers)
        if response.status_code == 422:
            print(hugo_theme)
            quit()
        if response.status_code == 200:
            theme.ETag = response.headers["ETag"].lstrip("W/")
            result = response.json()
            theme.commit_date = result["commit"]["author"]["date"]
            theme.commit_date_in_seconds = timegm(
                strptime(theme.commit_date, "%Y-%m-%dT%H:%M:%SZ")
            )
            theme.commit_sha = result["commit"]["tree"]["sha"]
            session.commit()
        elif response.status_code == 403:
            print(response.status_code, get_commit_info_for_hugo_themes.__name__)
            quit()
        elif response.status_code == 404:
            print(
                response.status_code,
                get_commit_info_for_hugo_themes.__name__,
                hugo_theme,
                api_call_url,
            )
        print(response.status_code, get_commit_info_for_hugo_themes.__name__)


def get_commit_info_for_hugo_themes_from_gitlab():
    session = sessionmaker(bind=engine)()
    theme_names_from_gitlab = get_gitlab_themes_name_list()
    # match = re.compile(r'(\.\d{3})(Z$)')
    for hugo_theme in theme_names_from_gitlab:
        theme = session.query(Hugothemes_from_gitlab).filter_by(name=hugo_theme).one()
        api_call_url = "https://gitlab.com/api/v4/projects/"
        api_call_url += f"{theme.gitlab_id}/repository/"
        api_call_url += f"commits/{theme.default_branch}"

        response = get(api_call_url)
        if response.status_code == 200:
            result = response.json()
            # theme.commit_date = (match.sub(r'\2', result[
            # 'created_at']))[0:19] + 'Z'
            theme.commit_date = result["created_at"][0:19] + "Z"
            theme.commit_date_in_seconds = timegm(
                strptime(theme.commit_date, "%Y-%m-%dT%H:%M:%SZ")
            )
            theme.commit_sha = result["id"]
            session.commit()
        elif response.status_code == 403:
            print(
                response.status_code,
                get_commit_info_for_hugo_themes_from_gitlab.__name__,
            )
            quit()
        elif response.status_code == 404:
            print(
                response.status_code,
                get_commit_info_for_hugo_themes_from_gitlab.__name__,
                hugo_theme,
            )
        print(
            response.status_code, get_commit_info_for_hugo_themes_from_gitlab.__name__
        )


def get_repo_info_for_hugo_themes():
    session = sessionmaker(bind=engine)()
    theme_names_from_github = get_github_themes_name_list()
    for hugo_theme in theme_names_from_github:
        theme = session.query(Hugothemes).filter_by(name=hugo_theme).one()
        theme_name = get_corrected_theme_name(theme.name)
        if "blox-tailwind" in theme_name:
            theme_name = "HugoBlox/hugo-blox-builder"
        api_call_url = "https://api.github.com/repos/" + theme_name

        if theme.repo_ETag is not None:
            headers["If-None-Match"] = theme.repo_ETag
        else:
            if "If-None-Match" in headers:
                del headers["If-None-Match"]

        if len(headers) == 0:
            response = get(api_call_url)
        else:
            response = get(api_call_url, headers=headers)
        if response.status_code == 200:
            theme.repo_ETag = response.headers["ETag"].lstrip("W/")
            result = response.json()
            theme.stargazers_count = result["stargazers_count"]
            theme.default_branch = result["default_branch"]
            session.commit()
        elif response.status_code == 403:
            print(response.status_code, get_repo_info_for_hugo_themes.__name__)
            quit()
        elif response.status_code == 404:
            print(
                response.status_code,
                get_repo_info_for_hugo_themes.__name__,
                hugo_theme,
                api_call_url,
                headers,
            )
        print(response.status_code, get_repo_info_for_hugo_themes.__name__)


def get_repo_info_for_hugo_themes_from_gitlab():
    session = sessionmaker(bind=engine)()
    theme_names_from_gitlab = get_gitlab_themes_name_list()
    for hugo_theme in theme_names_from_gitlab:
        theme = session.query(Hugothemes_from_gitlab).filter_by(name=hugo_theme).one()
        api_call_url = f"https://gitlab.com/api/v4/projects/{theme.gitlab_id}"
        response = get(api_call_url)
        if response.status_code == 200:
            result = response.json()
            if theme.star_count != result["star_count"]:
                theme.star_count = result["star_count"]
            if theme.default_branch != result["default_branch"]:
                theme.default_branch = result["default_branch"]
            session.commit()
        elif response.status_code == 403:
            print(
                response.status_code, get_repo_info_for_hugo_themes_from_gitlab.__name__
            )
            quit()
        elif response.status_code == 404:
            print(
                response.status_code,
                get_repo_info_for_hugo_themes_from_gitlab.__name__,
                hugo_theme,
            )
        print(response.status_code, get_repo_info_for_hugo_themes_from_gitlab.__name__)


def get_theme_toml_file_name(theme_name):
    if theme_name == "hugolify/hugolify-theme":
        return "theme.yml"
    if theme_name in THEMESYAMLTHEMES:
        return "theme.yaml"
    else:
        return "theme.toml"


def get_theme_dot_toml_for_each_hugo_themes():
    session = sessionmaker(bind=engine)()
    theme_names_from_github = get_github_themes_name_list()
    for hugo_theme in theme_names_from_github:
        theme = session.query(Hugothemes).filter_by(name=hugo_theme).one()
        theme_name = get_corrected_theme_name(theme.name)
        if theme.name == "gcushen/hugo-academic":
            theme_name = "wowchemy/starter-hugo-academic"
        api_call_url = "https://api.github.com/repos/"
        if "blox-tailwind" in theme_name:
            api_call_url += (
                "HugoBlox/hugo-blox-builder/contents/modules/blox-tailwind/theme.toml"
            )
        else:
            api_call_url += (
                f"{theme_name}/contents/{get_theme_toml_file_name(theme_name)}"
            )

        if theme.themes_toml_ETag is not None:
            headers["If-None-Match"] = theme.themes_toml_ETag
        else:
            if "If-None-Match" in headers:
                del headers["If-None-Match"]

            if len(headers) == 0:
                response = get(api_call_url)
            else:
                response = get(api_call_url, headers=headers)
            if response.status_code == 200:
                theme.themes_toml_ETag = response.headers["ETag"].lstrip("W/")
                result = response.json()
                theme.themes_toml_content = result["content"]
                session.commit()
            elif response.status_code == 403:
                print(
                    response.status_code,
                    get_theme_dot_toml_for_each_hugo_themes.__name__,
                )
                quit()
            elif response.status_code == 404:
                print(
                    response.status_code,
                    get_theme_dot_toml_for_each_hugo_themes.__name__,
                    hugo_theme,
                )
            print(
                response.status_code, get_theme_dot_toml_for_each_hugo_themes.__name__
            )


def get_theme_dot_toml_for_each_hugo_themes_from_gitlab():
    session = sessionmaker(bind=engine)()
    theme_names_from_gitlab = get_gitlab_themes_name_list()
    for hugo_theme in theme_names_from_gitlab:
        theme = session.query(Hugothemes_from_gitlab).filter_by(name=hugo_theme).one()
        api_call_url = "https://gitlab.com/api/v4/projects/"
        api_call_url += f"{theme.gitlab_id}/repository/files/"
        api_call_url += f"theme.toml?ref={theme.default_branch}"
        response = get(api_call_url)
        if response.status_code == 200:
            result = response.json()
            theme.themes_toml_content = result["content"]
            session.commit()
        elif response.status_code == 403:
            print(
                response.status_code,
                get_theme_dot_toml_for_each_hugo_themes_from_gitlab.__name__,
            )
            quit()
        elif response.status_code == 404:
            print(
                response.status_code,
                get_theme_dot_toml_for_each_hugo_themes_from_gitlab.__name__,
                hugo_theme,
            )
        print(
            response.status_code,
            get_theme_dot_toml_for_each_hugo_themes_from_gitlab.__name__,
        )


def coalesce_themes():
    session = sessionmaker(bind=engine)()
    theme_names_from_gitlab = get_gitlab_themes_name_list()
    for hugo_theme in theme_names_from_gitlab:
        htfgitlab = (
            session.query(Hugothemes_from_gitlab).filter_by(name=hugo_theme).one()
        )
        theme = session.query(Hugothemes).filter_by(name=hugo_theme).first()
        if theme is None:
            session.add(
                Hugothemes(
                    name=hugo_theme,
                    url=htfgitlab.url,
                    commit_sha=htfgitlab.commit_sha,
                    commit_date=htfgitlab.commit_date,
                    commit_date_in_seconds=htfgitlab.commit_date_in_seconds,
                    stargazers_count=htfgitlab.star_count,
                    themes_toml_content=htfgitlab.themes_toml_content,
                )
            )
        else:
            if theme.url != htfgitlab.url:
                theme.url = htfgitlab.url
            if theme.commit_sha != htfgitlab.commit_sha:
                theme.commit_sha = htfgitlab.commit_sha
            if theme.commit_date != htfgitlab.commit_date:
                theme.commit_date = htfgitlab.commit_date
            htfgitlab_cdis = htfgitlab.commit_date_in_seconds
            if theme.commit_date_in_seconds != htfgitlab_cdis:
                theme.commit_date_in_seconds = htfgitlab_cdis
            if theme.stargazers_count != htfgitlab.star_count:
                theme.stargazers_count = htfgitlab.star_count
            theme.themes_toml_content = htfgitlab.themes_toml_content
        session.commit()


def get_corrected_tags(tags):
    result = []
    correct = True
    for tag in tags:
        if len(tag) > 50:
            correct = False
    if not correct:
        for tag in tags:
            result += [x.lstrip() for x in tag.split(",")]
        return result
    else:
        return tags


def parse_themes_toml_for_each_hugo_themes():
    session = sessionmaker(bind=engine)()
    themes = [theme[0] for theme in session.query(Hugothemes.name).all()]
    match = re.compile(r"\s(\d+\.\d+\.\d+)\s")
    for hugo_theme in themes:
        theme = session.query(Hugothemes).filter_by(name=hugo_theme).one()
        if theme.themes_toml_content is not None:
            content = b64decode(theme.themes_toml_content).decode("utf-8")
            if theme.name == "Blackstareye/stargazer-layout":
                my_content = ""
                for line in content.splitlines():
                    if "hugoVersion" not in line:
                        my_content += line + "\n"
                content = my_content
            # put quotes around any unquoted double-dotted version numbers
            # (and add a newline afterwards)
            # because python toml libraries will error out on those
            theme_name = get_corrected_theme_name(theme.name)
            if theme_name in THEMESYAMLTHEMES:
                theme_toml = yaml.full_load(content)
            elif theme_name == "hugolify/hugolify-theme":
                theme_toml = yaml.full_load(content)
            else:
                theme_toml = toml.loads(match.sub(r'"\1"\n', content))
            if "tags" in theme_toml:
                if len(theme_toml["tags"]) > 0:
                    corrected_tags = get_corrected_tags(theme_toml["tags"])
                    tt = [tag.lower() for tag in corrected_tags if len(tag) > 1]
                    theme_tags = list(set(tt))
                    if theme.num_tags != len(theme_tags):
                        theme.num_tags = len(theme_tags)
                    if theme.num_tags > 0:
                        if theme.tags_list != str(theme_tags):
                            theme.tags_list = str(theme_tags)
                    else:
                        if theme.tags_list is not None:
                            theme.tags_list = None
                else:
                    if theme.tags_list is not None:
                        theme.tags_list = None
                    if theme.num_tags != 0:
                        theme.num_tags = 0
            else:
                if theme.tags_list is not None:
                    theme.tags_list = None
                if theme.num_tags != 0:
                    theme.num_tags = 0
            if "features" in theme_toml:
                if len(theme_toml["features"]) > 0:
                    tf = [
                        feature.lower()
                        for feature in theme_toml["features"]
                        if len(feature) > 1
                    ]
                    theme_features = list(set(tf))
                    if theme.num_features != len(theme_features):
                        theme.num_features = len(theme_features)
                    if theme.num_features > 0:
                        if theme.features_list != str(theme_features):
                            theme.features_list = str(theme_features)
                    else:
                        if theme.features_list is not None:
                            theme.features_list = None
                else:
                    if theme.features_list is not None:
                        theme.features_list = None
                    if theme.num_features != 0:
                        theme.num_features = 0
            else:
                if theme.features_list is not None:
                    theme.features_list = None
                if theme.num_features != 0:
                    theme.num_features = 0
            if "license" in theme_toml:
                if theme.theme_license != theme_toml["license"]:
                    theme.theme_license = theme_toml["license"]
            else:
                if theme.theme_license is not None:
                    theme.theme_license = None
                if "name" in theme_toml and theme_toml["name"] == "Henry Hugo Theme":
                    theme.theme_license = "MIT"
            if theme_toml_has_min_ver(theme_toml):
                corrected_mv = get_corrected_min_ver(
                    get_min_ver_from_theme_toml(theme_toml)
                )
                if theme.min_ver != corrected_mv:
                    theme.min_ver = corrected_mv
            else:
                if theme.min_ver is not None:
                    theme.min_ver = None
            if "description" in theme_toml:
                if theme.desc != theme_toml["description"]:
                    theme.desc = theme_toml["description"]
            else:
                if theme.desc is not None:
                    theme.desc = None
            if "name" in theme_toml:
                if theme.cname != theme_toml["name"]:
                    theme.cname = theme_toml["name"]
            else:
                if theme.cname is not None:
                    theme.cname = None
            if theme_name == "apvarun/digital-garden-hugo-theme":
                theme.cname = "Digital Garden Hugo"
        else:
            if theme.tags_list is not None:
                theme.tags_list = None
            if theme.num_tags != 0:
                theme.num_tags = 0
            if theme.features_list is not None:
                theme.features_list = None
            if theme.num_features != 0:
                theme.num_features = 0
            if theme.theme_license is not None:
                theme.theme_license = None
            if theme.min_ver is not None:
                theme.min_ver = None
            if theme.desc is not None:
                theme.desc = None
            if theme.cname is not None:
                theme.cname = None
        session.commit()


def get_min_ver_from_theme_toml(theme_toml):
    if "min_version" in theme_toml:
        return theme_toml["min_version"]
    if "module" in theme_toml:
        if "hugoVersion" in theme_toml["module"]:
            if "min" in theme_toml["module"]["hugoVersion"]:
                return theme_toml["module"]["hugoVersion"]["min"]
            if "min_version" in theme_toml["module"]["hugoVersion"]:
                return theme_toml["module"]["hugoVersion"]["min_version"]


def theme_toml_has_min_ver(theme_toml):
    if "min_version" in theme_toml:
        return True
    if "module" in theme_toml:
        if "hugoVersion" in theme_toml["module"]:
            if "min" in theme_toml["module"]["hugoVersion"]:
                return True
            if "min_version" in theme_toml["module"]["hugoVersion"]:
                return True
    return False


def get_corrected_min_ver(x):
    if "o" in str(x):
        return x.replace("o", "0")
    else:
        return x


def generate_report():
    session = sessionmaker(bind=engine)()
    hugo_themes = [
        {
            "name": theme.name,
            "commit": theme.commit_sha[0:6],
            "date": theme.commit_date[0:10],
            "date_in_seconds": theme.commit_date_in_seconds,
            "url": f"https://{theme.url}",
            "short_name": theme.name.split("/")[1],
            "num_stars": theme.stargazers_count,
            "tags": (
                literal_eval(theme.tags_list) if theme.tags_list is not None else []
            ),
            "features": (
                literal_eval(theme.features_list)
                if theme.features_list is not None
                else []
            ),
            "license": theme.theme_license if theme.theme_license is not None else "",
            "min_ver": theme.min_ver if theme.min_ver is not None else "",
            "desc": theme.desc if theme.desc is not None else "",
            "cname": (
                theme.cname if theme.cname is not None else theme.name.split("/")[1]
            ),
        }
        for theme in session.query(Hugothemes).all()
    ]
    output = template.render(themes=hugo_themes)
    index_page = open("hugo-themes-report/hugo-themes-report.html", "w")
    index_page.write(output)
    index_page.close()


if __name__ == "__main__":
    """
    or test with
    `
    python3 -c'import rank_hugo_themes; rank_hugo_themes
    .parse_themes_toml_for_each_hugo_themes()
    ; rank_hugo_themes.generate_report()'
    `
    """
    dedup_database()
    get_hugo_themes_list()
    if len(THEMESLIST) > 300:
        clean_up()
        parse_hugo_themes_list()
        parse_gitlab_hugo_themes_list()
        get_gitlab_project_ids()
        get_repo_info_for_hugo_themes()
        get_repo_info_for_hugo_themes_from_gitlab()
        get_commit_info_for_hugo_themes()
        get_commit_info_for_hugo_themes_from_gitlab()
        get_theme_dot_toml_for_each_hugo_themes()
        get_theme_dot_toml_for_each_hugo_themes_from_gitlab()
        coalesce_themes()
        parse_themes_toml_for_each_hugo_themes()
        generate_report()
