#!/usr/bin/env python3
# rank_hugo_themes.py

import re
import toml 
from calendar import timegm
from time import strptime
from requests import get
from sqlite3 import connect
from json import loads as json_loads
from sys import argv as sys_argv
from base64 import b64decode
from ast import literal_eval

DATABASENAME='hugothemes.db'
# CREATE TABLE hugothemes (name varchar unique, ETag text, url text, jsondump text, commit_sha text, commit_date text, commit_date_in_seconds int, repo_ETag text, stargazers_count int, themes_toml_ETag text, themes_toml_content text, tags_list text, num_tags int);
# CREATE TABLE tags (tag varchar unique, theme_list text, num_themes int);
THEMESLISTREPO='gohugoio/hugoThemes'

if len(sys_argv) == 2:
    headers = { 'Authorization' : 'token '+sys_argv[1] }
else:
    headers = {}


def get_hugo_themes_list():
    dbconnection = connect(DATABASENAME)
    cursor = dbconnection.cursor()
    cursor.execute("select ETag from hugothemes where name=?",(THEMESLISTREPO,))
    old_ETag = cursor.fetchone()[0]
    api_call_url = "https://api.github.com/repos/"+THEMESLISTREPO+"/contents"

    if old_ETag != None:
        headers['If-None-Match'] = old_ETag
    else:
        if 'If-None-Match' in headers:
            del headers['If-None-Match']

    if len(headers) == 0:
        response = get(api_call_url)
    else:
        response = get(api_call_url, headers=headers)
    if response.status_code == 200:
        ETag = response.headers['ETag']
        sql = "update hugothemes set ETag=?,url=?,jsondump=? where name=?"
        values=(ETag,api_call_url,response.text,THEMESLISTREPO)
        cursor.execute(sql,values)
        dbconnection.commit()
    elif response.status_code == 403:
        print(response.status_code)
        cursor.close()
        dbconnection.close()
        write_reports()
        quit()
    print(response.status_code)
    cursor.close()
    dbconnection.close()


def clean_up():
    dbconnection = connect(DATABASENAME)
    cursor = dbconnection.cursor()
    cursor.execute("select jsondump from hugothemes where name=?",(THEMESLISTREPO,))
    themes_json_string = cursor.fetchone()[0]
    themes_json = json_loads(themes_json_string)
    new_name_list = []
    for theme in themes_json:
        if theme['git_url']:
            if 'gohugoio' not in theme['git_url']:
                split_html_url = theme['html_url'].split('/')
                new_short_name = split_html_url[3]+'/'+split_html_url[4]
                new_name_list.append(new_short_name)
    cursor.execute("select name from hugothemes where name!=?",(THEMESLISTREPO,))
    old_name_list = cursor.fetchall()
    for name in old_name_list:
        if name[0] not in new_name_list:
            cursor.execute("delete from hugothemes where name=?",(name[0],))
            dbconnection.commit()
    cursor.close()
    dbconnection.close()


def parse_hugo_themes_list():
    dbconnection = connect(DATABASENAME)
    cursor = dbconnection.cursor()
    cursor.execute("select jsondump from hugothemes where name=?",(THEMESLISTREPO,))
    themes_json_string = cursor.fetchone()[0]
    themes_json = json_loads(themes_json_string)
    for x in themes_json:
        if x['git_url']:
            if 'gohugoio' not in x['git_url']:
                theme_git_url = x['html_url'][:-46]
                theme_git_name = theme_git_url[19:]
                cursor.execute("insert or ignore into hugothemes (name) values (?)",[theme_git_name])
                dbconnection.commit()
                sql = "update hugothemes set url=?,commit_sha=? where name=?"
                values=(theme_git_url,x['sha'],theme_git_name)
                cursor.execute(sql,values)
                dbconnection.commit()
    cursor.close()
    dbconnection.close()


def get_commit_info_for_hugo_themes():
    dbconnection = connect(DATABASENAME)
    cursor = dbconnection.cursor()
    cursor.execute("select name,ETag,url,commit_sha from hugothemes where name!=?",(THEMESLISTREPO,))
    hugo_themes_list = cursor.fetchall()
    for theme in hugo_themes_list:
        name,old_ETag,url,commit_sha = theme
        api_call_url = 'https://api.github.com/repos/' + name + '/commits/' + commit_sha

        if old_ETag != None:
            headers['If-None-Match'] = old_ETag
        else:
            if 'If-None-Match' in headers:
                del headers['If-None-Match']

        if len(headers) == 0:
            response = get(api_call_url)
        else:
            response = get(api_call_url, headers=headers)
        if response.status_code == 200:
            ETag = response.headers['ETag']
            result = response.json()
            commit_date = result['commit']['author']['date']
            commit_date_in_seconds = timegm(strptime(commit_date,'%Y-%m-%dT%H:%M:%SZ'))
            sql = "update hugothemes set ETag=?,commit_date=?,commit_date_in_seconds=? where name=?"
            values=(ETag,commit_date,commit_date_in_seconds,name)
            cursor.execute(sql,values)
            dbconnection.commit()
        elif response.status_code == 403:
            print(response.status_code)
            cursor.close()
            dbconnection.close()
            write_reports()
            quit()
        print(response.status_code)
    cursor.close()
    dbconnection.close()
    

def get_stargazer_count_for_hugo_themes():
    dbconnection = connect(DATABASENAME)
    cursor = dbconnection.cursor()
    cursor.execute("select name,repo_ETag from hugothemes where name!=?",(THEMESLISTREPO,))
    hugo_themes_list = cursor.fetchall()
    for theme in hugo_themes_list:
        name,old_ETag = theme
        api_call_url = 'https://api.github.com/repos/' + name

        if old_ETag != None:
            headers['If-None-Match'] = old_ETag
        else:
            if 'If-None-Match' in headers:
                del headers['If-None-Match']

        if len(headers) == 0:
            response = get(api_call_url)
        else:
            response = get(api_call_url, headers=headers)
        if response.status_code == 200:
            repo_ETag = response.headers['ETag']
            result = response.json()
            stargazers_count = result['stargazers_count']
            sql = "update hugothemes set repo_ETag=?,stargazers_count=? where name=?"
            values=(repo_ETag,stargazers_count,name)
            cursor.execute(sql,values)
            dbconnection.commit()
        elif response.status_code == 403:
            print(response.status_code)
            cursor.close()
            dbconnection.close()
            write_reports()
            quit()
        print(response.status_code)
    cursor.close()
    dbconnection.close()


def get_theme_dot_toml_for_each_hugo_themes():
    dbconnection = connect(DATABASENAME)
    cursor = dbconnection.cursor()
    cursor.execute("select name,themes_toml_ETag from hugothemes where name!=?",(THEMESLISTREPO,))
    hugo_themes_list = cursor.fetchall()
    for theme in hugo_themes_list:
        name,old_ETag = theme
        api_call_url = "https://api.github.com/repos/"+name+"/contents/theme.toml"

        if old_ETag != None:
            headers['If-None-Match'] = old_ETag
        else:
            if 'If-None-Match' in headers:
                del headers['If-None-Match']

        if len(headers) == 0:
            response = get(api_call_url)
        else:
            response = get(api_call_url, headers=headers)
        if response.status_code == 200:
            themes_toml_ETag = response.headers['ETag']
            result = response.json()
            themes_toml_content = result['content']
            sql = "update hugothemes set themes_toml_ETag=?,themes_toml_content=? where name=?"
            values=(themes_toml_ETag,themes_toml_content,name)
            cursor.execute(sql,values)
            dbconnection.commit()
        elif response.status_code == 403:
            print(response.status_code)
            cursor.close()
            dbconnection.close()
            write_reports()
            quit()
        print(response.status_code)
    cursor.close()
    dbconnection.close()


def update_tags_list_for_each_hugo_themes():
    dbconnection = connect(DATABASENAME)
    cursor = dbconnection.cursor()
    cursor.execute("select name,themes_toml_content from hugothemes where name!=?",(THEMESLISTREPO,))
    hugo_themes_list = cursor.fetchall()
    for theme in hugo_themes_list:
        if theme[1] != None:
            content = b64decode(theme[1]).decode('utf-8')
            # put quotes around any unquoted double-dotted version numbers
            # because python toml libraries will error out on those
            theme_toml = toml.loads(re.sub(r'\s(\d+\.\d+\.\d+)\s',r'"\1"',content))
            if 'tags' in theme_toml:
                if len(theme_toml['tags']) > 0:
                    theme_tags = [tag.lower() for tag in theme_toml['tags'] if len(tag) > 0]
                    num_tags = len(theme_tags)
                    if num_tags > 0:
                        tag_list = str(theme_tags)
                    else:
                        tag_list = None
                else:
                    tag_list = None
                    num_tags = 0
            else:
                tag_list = None
                num_tags = 0
        else:
            tag_list = None
            num_tags = 0
        sql = "update hugothemes set tags_list=?,num_tags=? where name=?"
        values=(tag_list,num_tags,theme[0])
        cursor.execute(sql,values)
        dbconnection.commit()
    cursor.close()
    dbconnection.close()


def update_tag_table():
    dbconnection = connect(DATABASENAME)
    cursor = dbconnection.cursor()
    cursor.execute("select name,tags_list from hugothemes where name!=?",(THEMESLISTREPO,))
    hugo_themes_list = cursor.fetchall()
    tags_list = []
    for theme in hugo_themes_list:
        if theme[1] != None:
            tags = literal_eval(theme[1])
            for tag in tags:
                if len(tag) > 0:
                    if tag not in tags_list:
                        tags_list.append(tag)

    for tag in tags_list:
        cursor.execute("insert or ignore into tags (tag) values (?)",[tag])
        dbconnection.commit()
        theme_list = []
        for theme in hugo_themes_list:
            if theme[1] != None:
                tags = literal_eval(theme[1])
                if tag in tags:
                    theme_list.append(theme[0])
        sql = "update tags set theme_list=?,num_themes=? where tag=?"
        values=(str(theme_list),len(theme_list),tag)
        cursor.execute(sql,values)
        dbconnection.commit()

    cursor.close()
    dbconnection.close()


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
        row = "\t\t\t\t<tr><td scope='row'>"+"<a href="+theme[4]+">"+name+"</a>""</td>"
        row += "<td nowrap>"+theme[2][:10]+"</td>"
        row += "<td align='right' nowrap style='padding-left:1em;'>"+str(theme[3])+'&#x2605'+"</td>"
        row += "<td align='right' style='padding-left:1em;'>"+theme[1][:6]+"</td></tr>\n"
        table += row
    table += "\t\t\t</tbody>\n\t\t</table>\n\t</div>\n" 
    return table


def make_section(section_info):
    if section_info[3] > 10:
        section = make_nav_buttons((section_info[0],'by-date',section_info[3]))
        section += make_table((section_info[1],section_info[0],'by-date'))
        section += make_nav_buttons((section_info[0],'by-stars',section_info[3]))
        section += make_table((section_info[2],section_info[0],'by-stars'))
    else:
        section = make_nav_buttons((section_info[0],'by-date',section_info[3]))
        section += make_table((section_info[1],section_info[0],'by-date'))
    return section


def write_reports():
    dbconnection = connect(DATABASENAME)
    cursor = dbconnection.cursor()
    cursor.execute("select name,commit_sha,commit_date,stargazers_count,url from hugothemes where name!=? order by commit_date_in_seconds DESC",(THEMESLISTREPO,))
    themes_bydate_list = cursor.fetchall()
    cursor.execute("select name,commit_sha,commit_date,stargazers_count,url from hugothemes where name!=? order by stargazers_count DESC",(THEMESLISTREPO,))
    themes_bystars_list = cursor.fetchall()
    themes = [theme[0] for theme in themes_bystars_list]
    tags_list = [('all',str(themes),len(themes))]
    cursor.execute("select tag,theme_list,num_themes from tags where num_themes > 2 order by num_themes DESC")
    for row in cursor:
        tags_list.append(row)
    cursor.close()
    dbconnection.close()

    reportpage = "<!DOCTYPE html>\n<html lang='en'>\n"
    reportpage += "\t<head>\n\t\t<title>Hugo Themes Report</title>\n\t\t<meta charset='utf-8'>"
    reportpage += "\n\t\t<meta name='viewport' content='width=device-width, initial-scale=1'>\n"
    reportpage += "\t\t<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css' "
    reportpage += "integrity='sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm' crossorigin='anonymous'>\n\t</head>\n"
    reportpage += "\t<body>\n" 

    reportpage += make_section(('all',themes_bydate_list,themes_bystars_list,len(themes_bydate_list)))
    reportpage += make_buttons(tags_list)
    for tag in tags_list[1:]:
        tag_theme_list = literal_eval(tag[1])
        bydate_list = [theme for theme in themes_bydate_list if theme[0] in tag_theme_list]
        bystars_list = [theme for theme in themes_bystars_list if theme[0] in tag_theme_list]
        reportpage += make_section((tag[0],bydate_list,bystars_list,tag[2]))

    reportpage += "\t</body>" 
    reportpage += "\n</html>"
    by_date = open('hugo-themes-report/hugo-themes-report.html','w')
    by_date.write(reportpage)
    by_date.close()


if __name__=="__main__":
    get_hugo_themes_list()
    clean_up()
    parse_hugo_themes_list()
    get_commit_info_for_hugo_themes()
    get_stargazer_count_for_hugo_themes()
    get_theme_dot_toml_for_each_hugo_themes()
    update_tags_list_for_each_hugo_themes()
    write_reports()
    """
    """
