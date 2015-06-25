# coding=utf-8
import sys
from subprocess import check_output, call


def main(date):
    output = check_output('git branch|grep -v master', shell=True)
    for branch in output.split('\n'):
        branch = branch.strip()
        if '*' in branch:
            continue
        p = check_output(
            'git log --since="{0}" -s {1}'.format(date, branch), shell=True)
        if not p:
            call('git branch -D {}'.format(branch), shell=True)
            call('git push --delete --no-verify origin {}'.format(branch),
                 shell=True)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        date_ = '2.weeks'
    else:
        date_ = sys.argv[1]
    main(date_)
