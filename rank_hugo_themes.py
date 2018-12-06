#!/usr/bin/env python36
# rank_hugo_themes.py

# import sqlite3,json,sys,calendar,time,requests
from calendar import timegm
from time import strptime
from requests import get
from sqlite3 import connect
from json import loads as json_loads
from sys import argv as sys_argv

DATABASENAME='hugothemes.db'
# CREATE TABLE hugothemes (name varchar unique, ETag text, url text, jsondump text, commit_sha text, commit_date text, commit_date_in_seconds int, repo_ETag text, stargazers_count int);
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

def write_reports():
    dbconnection = connect(DATABASENAME)
    cursor = dbconnection.cursor()
    cursor.execute("select name,commit_sha,commit_date,stargazers_count,url from hugothemes where name!=? order by commit_date_in_seconds DESC",(THEMESLISTREPO,))
    hugo_themes_list = cursor.fetchall()
    cursor.close()
    dbconnection.close()
    bycommitTable = "<!DOCTYPE html>\n<html lang='en'>\n"
    bycommitTable += "\t<head>\n\t\t<title>Hugo Themes Report Order By Commit Date</title>\n\t\t<meta charset='utf-8'>"
    bycommitTable += "\n\t\t<meta name='viewport' content='width=device-width, initial-scale=1'>\n"
    bycommitTable += "\t\t<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css' integrity='sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u' crossorigin='anonymous'>\n\t</head>\n"
    bycommitTable += "\t<div style='text-align:center;font-size:200%;'><a style='text-decoration:none;'href=\"hugo-themes-by-num-stars.html\">(Switch-to-Order-by-Num-Stars)</a></div>\n"
    bycommitTable +="\t<div class='container'>\n\t\t<table class='table monospace'>\n\t\t\t<thead><tr><th scope='col'>Name</th><th scope='col'>Date</th></tr></thead>\n\t\t\t<tbody>\n"
    for theme in hugo_themes_list:
        name = theme[0].split('/')[1]
        row = "\t\t\t\t<tr><td scope='row'>"+"<a href="+theme[4]+">"+name+"</a>""</td>"
        row += "<td nowrap>"+theme[2][:10]+"</td>"
        row += "<td align='right' nowrap style='padding-left:1em;'>"+str(theme[3])+'&#x2605'+"</td>"
        row += "<td align='right' style='padding-left:1em;'>"+theme[1][:6]+"</td></tr>\n"
        bycommitTable += row
    bycommitTable += "\t\t\t</tbody>\n\t\t</table>\n\t</div>\n</html>"
    by_date = open('hugo-themes-report/hugo-themes-by-last-commit-date.html','w')
    by_date.write(bycommitTable)
    by_date.close()

    dbconnection = connect(DATABASENAME)
    cursor = dbconnection.cursor()
    cursor.execute("select name,commit_sha,commit_date,stargazers_count,url from hugothemes where name!=? order by stargazers_count DESC",(THEMESLISTREPO,))
    hugo_themes_list = cursor.fetchall()
    cursor.close()
    dbconnection.close()
    bystarsTable = "<!DOCTYPE html>\n<html lang='en'>\n"
    bystarsTable += "\t<head>\n\t\t<title>Hugo Themes Report Order By Num Stars</title>\n\t\t<meta charset='utf-8'>"
    bystarsTable += "\n\t\t<meta name='viewport' content='width=device-width, initial-scale=1'>\n"
    bystarsTable += "\t\t<link rel='stylesheet' type='text/css' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css' integrity='sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u' crossorigin='anonymous'>\n\t</head>\n"
    bystarsTable += "\t<div style='text-align:center;font-size:200%;'><a style='text-decoration:none;'href=\"hugo-themes-by-last-commit-date.html\">(Switch-Order-by-Commit-Date)</a></div>\n"
    bystarsTable += "\t<div class='container'>\n\t\t<table class='table monospace'>\n\t\t\t<thead><tr><th scope='col'>Name</th><th scope='col'>Date</th></tr></thead>\n\t\t\t<tbody>\n"
    for theme in hugo_themes_list:
        name = theme[0].split('/')[1]
        row = "\t\t\t\t<tr><td scope='row'>"+"<a href="+theme[4]+">"+name+"</a>""</td>"
        row += "<td nowrap>"+theme[2][:10]+"</td>"
        row += "<td align='right' nowrap style='padding-left:1em;'>"+str(theme[3])+'&#x2605'+"</td>"
        row += "<td align='right' style='padding-left:1em;'>"+theme[1][:6]+"</td></tr>\n"
        bystarsTable += row
    bystarsTable += "\t\t\t</tbody>\n\t\t</table>\n\t</div>\n</html>"
    by_date = open('hugo-themes-report/hugo-themes-by-num-stars.html','w')
    by_date.write(bystarsTable)
    by_date.close()


if __name__=="__main__":
    get_hugo_themes_list()
    clean_up()
    parse_hugo_themes_list()
    get_commit_info_for_hugo_themes()
    get_stargazer_count_for_hugo_themes()
    write_reports()
