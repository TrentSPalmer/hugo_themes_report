import re
MATCH = re.compile(r'\d+')


def compare_jk(j, k):
    if j == k: return 0
    else: return 1 if j < k else -1


def semver_split(item):
    split_list = [MATCH.search(i).group() if
                  len(item) > 0 else '0' for i in item.split('.')]
    if len(split_list) == 1: split_list.append('0')
    if len(split_list) == 2: split_list.append('0')
    return [int(x) for x in split_list]


def compare_theme(x, y, sort_key):
    if sort_key == 'sortByName':
        if y['name'].lower() == x['name'].lower():
            return compare_jk(x['name'], y['name'])
        else:
            return compare_jk(y['name'].lower(), x['name'].lower())

    elif sort_key == 'sortByStars':
        return compare_jk(int(x['stars']), int(y['stars']))

    elif sort_key == 'sortByMinVer':
        x_list = semver_split(x['min_ver'])
        y_list = semver_split(y['min_ver'])
        return compare_jk(x_list, y_list)

    elif sort_key == 'sortByDate':
        return compare_jk(x['date'], y['date'])

    elif sort_key == 'sortByLicense':
        return compare_jk(y['license'].lower(), x['license'].lower())

    else:
        return 0


def theme_compare(a, b, y):
    if len(y) == 0: return -1
    rslt = compare_theme(a, b, y[0])
    return theme_compare(a, b, y[1:]) if rslt == 0 else rslt


def cname_compare(a, b):
    if a.cname.lower() == b.cname.lower():
        return 1 if a.cname < b.cname else -1
    else:
        return -1 if a.cname.lower() < b.cname.lower() else 1
