"""
little util to make it easier to compare branches that have been reordered /
forced pushed / etc.

using commit names to find the same commits in the series, not hashes.
"""
import sys
import re
from git import Repo
from jinja2 import Environment, FileSystemLoader
templateLoader = FileSystemLoader(searchpath="./")
templateEnv = Environment(loader=templateLoader)


def clean(body):
    """
    remove lines that aren't helpful
    """
    res = []
    for line in body.split('\n'):
        if re.match(r'commit [a-f0-9]*$', line):
            continue

        if re.match(r'index [a-f0-9. ]*$', line):
            continue

        if re.match(r'Date:[\ta-zA-Z0-9\+\-: ]*$', line):
            continue

        res.append(line)

    return '\n'.join(res)


def main():
    r = Repo(sys.argv[1])
    a = sys.argv[2]
    b = sys.argv[3]
    branches = [a, b]
    merge_base = r.merge_base(*branches)[0]

    to_check = {}

    for branch in branches:
        curr = {}
        for commit in r.iter_commits(branch):
            curr[commit.summary] = commit
            if commit == merge_base:
                break
        to_check[branch] = curr

    res = {
        'branch_a': a,
        'branch_b': b,
        'parent': merge_base
    }

    to_check_more = []

    # go through to_check and see what is actually different.
    found = []
    for commit in to_check[a].keys():
        if commit not in to_check[b].keys():
            found.append(commit)
        else:
            to_check_more.append(commit)

    res['a_not_in_b'] = found

    found = []
    for commit in to_check[b].keys():
        if commit not in to_check[a].keys():
            found.append(commit)
        else:
            to_check_more.append(commit)

    res['b_not_in_a'] = found

    res['modified'] = []
    res['same'] = []

    # now we have a list of commits that both have, so we want to check these
    # to find any differences.
    to_check_more = set(to_check_more)
    for commit in to_check_more:
        a_ver = r.git.show(to_check[a][commit])
        b_ver = r.git.show(to_check[b][commit])
        if clean(a_ver) != clean(b_ver):
            res['modified'].append((commit, a_ver, b_ver))
        else:
            res['same'].append(commit)

    # now display it as html with the template

    print(templateEnv.get_template('template.html').render(res))


if __name__ == "__main__":
    main()
