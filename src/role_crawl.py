"""
Given a specific Chef role, and a root directory containing three sub-directories (cookbooks/data_bags/roles),
this application will recursively walk (okay, *crawl*) through the hierarchy of sub-roles and recipes,
then print out the full structure.

(Verbose mode will also print out references to additional file types, such as data_bags,
templates, included packages or pip-installed packages).

Python 2.7+

ASCII art, alas, is absent.
"""

import os

from role_tools import *

PROG_NAME = os.path.basename(__file__).replace('.py', '')

# TEST_ROLE = "role[jenkins-slave-appserv]"
MY_ROOT = r"F:\Python\Role_Crawl\devops"
# TODO - read knife.rb config for directory root

ROLES_DIR = 'roles'
COOKBOOKS_DIR = 'cookbooks'
RECIPES_DIR = 'recipes'
# TODO - set these sub-directories in command-line parameters?


class Role(object):
    def __init__(self, root_dir, role_str):
        """
            :param root_dir: root directory where cookbooks, etc are.
            :param role_str: in the form of role[jenkins-slave-appserv]
        """
        self.roles_dir = os.path.join(root_dir, ROLES_DIR)
        self.full_role = role_str
        possible_role = re.search(role_ex, role_str)
        if not possible_role:
            print "Problems parsing initial role = <{0}>".format(role_str)
            sys.exit(1)
        self.role_name = possible_role.group(1)

        # Get text lines from file
        role_path = os.path.join(self.roles_dir, self.role_name) + '.json'
        ref_lines = grab_file_lines(role_path)

        # Get sub-roles and recipes as strings
        ref_list = [re.search(rec_ex, line.strip()).groups() for line in ref_lines
                    if re.search(rec_ex, line.strip())]
        self.external_refs_str = ref_list

        # Convert strings to Nodes
        self.nodes = []
        for ref_type, ref_name in ref_list:
            if ref_type == 'role':
                foo = Role(root_dir, "role[%s]" % ref_name)  # Yeah, this needs fixing.
                self.nodes.append(foo)
            elif ref_type == 'recipe':
                foo = Recipe(root_dir, "recipe[%s]" % ref_name)  # Yeah, this needs fixing.
                self.nodes.append(foo)

    def __repr__(self, tab_level=0, verbose=False):
        name_list = []
        my_name = "{pad_char:>{spaces}}role: <{rname}>".format(pad_char='', spaces=4 * tab_level, rname=self.role_name)
        name_list.append(my_name)

        for x in self.nodes:
            full_name = x.__repr__(tab_level + 1, verbose)
            name_list.extend(full_name)

        return name_list


class Recipe(object):
    def __init__(self, root_dir, ref_str):
        self.books_dir = os.path.join(root_dir, COOKBOOKS_DIR)
        self.full_ref = ref_str
        possible_book = re.search(book_ex, ref_str)
        if not possible_book:
            print "Problems parsing initial book = <{0}>".format(ref_str)
            sys.exit(1)
        self.book_name = possible_book.group(1)

        # possible_recipe = re.search(book_ex, ref_str)
        self.recipe_name = possible_book.group(2) if len(possible_book.group(2)) else "default"

        # Get text lines from file
        repo = os.path.join(self.books_dir, self.book_name)
        sub_dir = os.path.join(repo, RECIPES_DIR)
        book_path = os.path.join(sub_dir, self.recipe_name) + '.rb'
        file_lines = grab_file_lines(book_path)

        # Find "include_recipe" lines
        ref_list = filter_refs(file_lines, include_ex)

        # Find "package" lines
        ref2_list = filter_refs(file_lines, package_ex)
        ref2_list = [ref for ref in ref2_list if ' do' not in ref]
        ref_list.extend(ref2_list)

        # Find "source *.erb" lines
        ref3_list = filter_refs(file_lines, source_ex)
        ref_list.extend(ref3_list)

        # Find data_bags
        ref4_list = filter_refs(file_lines, databag_ex)
        ref_list.extend(ref4_list)

        self.includes = ref_list

    def __repr__(self, tab_level=0, verbose=False):
        name_list = []
        fmt = "{pad_char:>{spaces}}recipe: <{bname}::{rname}>"
        my_name = fmt.format(pad_char='', spaces=4 * tab_level, bname=self.book_name, rname=self.recipe_name)
        name_list.append(my_name)

        if not verbose:
            return name_list

        for inc in self.includes:
            fmt = "{pad_char:>{spaces}}[{iname}]"
            full_name = fmt.format(pad_char='', spaces=4 * (tab_level + 1), iname=inc)
            name_list.append(full_name)

        return name_list


def crawl(root_dir, test_role, verbose=False):
    node_tree = Role(root_dir, test_role)
    node_list = node_tree.__repr__(tab_level=0, verbose=verbose)

    for x in node_list:
        print x


def run_it():
    """ You have to run() before you can crawl() """
    good_args = main_parsing()
    crawl(good_args.dir, good_args.role, good_args.verbose)


if __name__ == '__main__':
    run_it()
