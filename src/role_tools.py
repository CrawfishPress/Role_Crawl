import argparse
from argparse import HelpFormatter
import os
import sys

from role_ex import *

ROOT = os.path.expanduser("~/chef-repo")


def main_parsing():
    usage = """Usage: specify a chef-role, and an optional root-directory.
    The output will be a hierarchical list of roles and recipes,
    and optionally, all external file references (templates and databags).

    """

    hp = lambda prog: HelpFormatter(prog, max_help_position=50, width=120)
#     def hp(*args, **kwargs):  # pep8 says use a def, not lambda here, but it's bombing, no clue why.
#         HelpFormatter(hp, max_help_position=50, width=120)
    parser = argparse.ArgumentParser(description=usage, formatter_class=hp)

    parser.add_argument('-r', '--role', help='chef-role to crawl (required)')
    parser.add_argument('-d', '--dir', default=ROOT, help='root directory where cookbooks/databags/roles are stored (optional)')
    parser.add_argument('-v', '--verbose', action="store_true", help='include all external references, such as templates and databags')
    args = parser.parse_args()

    # You would think an empty argument list would *default* to printing help, but no...
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if not args.role:
        print 'chef-role is required'
        sys.exit(1)

    return args


def grab_file_lines(file_path):
    try:
        file_fp = open(file_path)
        file_lines = [line.strip() for line in file_fp.readlines() if len(line.strip())]
        file_fp.close()
    except IOError as e:
        print e
        sys.exit(1)

    return file_lines


def filter_refs(ref_lines, ref_regex):
    ref_list = [re.search(ref_regex, line).group(1) for line in ref_lines
                if re.search(ref_regex, line)]

    ref_list = list(set(ref_list))

    return ref_list


if __name__ == "__main__":
    print "this is a support module for role_craw.py"
