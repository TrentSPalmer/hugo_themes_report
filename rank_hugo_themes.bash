#!/bin/bash
# rank_hugo_themes.bash

REPOS_API_URL="https://api.github.com/repos"

# initialize an empty array
HUGO_THEME_REPOS=

# and now populate HUGO_THEME_REPOS list
for hugo_theme_commit_url in \
    "$(curl -s https://api.github.com/repos/gohugoio/hugoThemes/contents/ \
    | grep git_url | grep -v null | grep -v gohugoio | awk '{print $2}' \
    | sed -e 's/git\/trees/commits/g' | sed -e 's/,$//g')"
do
    HUGO_THEME_REPOS+=($hugo_theme_commit_url)
done

HUGO_THEME_REPOS_LIST_LENGTH="${#HUGO_THEME_REPOS[@]}"

# Test Make Sure We Have A HUGO_THEME_REPOS list
[[ "${HUGO_THEME_REPOS_LIST_LENGTH}" -gt 20 ]] || { echo "error: HUGO_THEME_REPOS_LIST not parsed" ; exit ;}

# just a few at a time because of github api limit

for num in {1..4}
do
    # pick a random hugo theme repo
    url=""
    url=${HUGO_THEME_REPOS[$((RANDOM%$HUGO_THEME_REPOS_LIST_LENGTH))]}
    [[ -n "${url}" ]] || continue

    hugo_theme_user=""
    hugo_theme_user=$(echo $url | awk -F"/" '{print $5}')
    [[ "${#hugo_theme_user}" -gt 2 ]] || continue

    hugo_theme=""
    hugo_theme=$(echo $url | awk -F"/" '{print $6}')
    [[ "${#hugo_theme_user}" -gt 2 ]] || continue

    commit_hash=""
    commit_hash=$(echo $url | awk -F"/" '{print $8}' | sed -e 's/"//g')
    [[ "${#commit_hash}" -gt 2 ]] || continue
    
    stars=""
    stars=$(curl -s "${REPOS_API_URL}/${hugo_theme_user}/${hugo_theme}" \
        | grep stargazers_count | head -1 | awk '{print $2}' \
        | sed -e 's/,$//g')
    [[ -n "${stars}" ]] || continue

    last_commit_date=""
    last_commit_date=$(curl -s \
        "${REPOS_API_URL}/${hugo_theme_user}/${hugo_theme}/commits/${commit_hash}" \
        | grep date | head -1 | awk '{print $2}' | sed -e 's/"//g')
    [[ -n "${last_commit_date}" ]] || continue
    printf "%-30s %-30s %-30s %30s\n" "$stars" "$hugo_theme" \
        "$hugo_theme_user" "$last_commit_date" >> ~/bin/rank_hugo_themes.log
done

# modify to taste
sort -rn ~/bin/rank_hugo_themes.log | uniq > ~/bin/rank_hugo_themes.report
