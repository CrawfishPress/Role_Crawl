import re

ROLE_REGEX = r"""   # Matches "role[users-stuff]"
    role
    [\s]*           # Optional whitespace - not that we *use* whitespace there - just habit to allow for it...
    \[              # I considered adding optional whitespace inside the brackets, but we don't do that either, so...
    ([\w-]+)        # Capture the role-name
    \]
"""

ROLE_RECIPE_REGEX = r"""    # Matches "role[users]"
                            #   or "recipe[jenkins]"
                            #   or "recipe[jenkins::build-dependencies]"
    (role|recipe)           # Capture the type: role or recipe
    [\s]*
    \[
    ([\w:-]+)               # Capture the object-name
    \]
"""

BOOK_REGEX = r"""   # Matches "recipe[jenkins]" or "recipe[jenkins::build-dependencies]"
    recipe
    [\s]*
    \[
    ([\w-]+)        # Capture the book-name
    :{0,2}          # Matches 0,1,2 colons. One colon is a syntax error, but this isn't a Ruby syntax-checker...
    ([\w-]*)        # Capture the recipe-name
    \]
"""

PACKAGE_RECIPE_REGEX = r""" # Matches "package 'git'" - everything is captured
    (package
    [\s]+
    .*)
"""

INCLUDE_RECIPE_REGEX = r""" # Matches "include_recipe 'jenkins'" or "include_recipe 'jenkins::package'"
                            # - everything is captured
    (include_recipe.*)
"""

SOURCE_RECIPE_REGEX = r"""  # Matches "source 'aws-config.erb'" - everything is captured
    (source
    [\s]+
    .*
    erb
    .?)
"""

DATA_BAG_RECIPE_REGEX = r"""  # Matches "data_bag_item('aws-credentials', node['jenkins']['bootstrap_key'])" - everything is captured
    (data_bag_item.*)
"""

role_ex = re.compile(ROLE_REGEX, re.VERBOSE)
rec_ex = re.compile(ROLE_RECIPE_REGEX, re.VERBOSE)
book_ex = re.compile(BOOK_REGEX, re.VERBOSE)
include_ex = re.compile(INCLUDE_RECIPE_REGEX, re.VERBOSE)
package_ex = re.compile(PACKAGE_RECIPE_REGEX, re.VERBOSE)
source_ex = re.compile(SOURCE_RECIPE_REGEX, re.VERBOSE)
databag_ex = re.compile(DATA_BAG_RECIPE_REGEX, re.VERBOSE)


if __name__ == "__main__":
    print "this is a support module for role_craw.py"
