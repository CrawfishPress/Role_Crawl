Role_crawl
==========

Given a specific _Chef role_, and an optional _root directory_ containing three sub-directories (cookbooks/data_bags/roles),
this application will recursively walk (okay, _crawl_) through the hierarchy of sub-roles and recipes, 
then print out the full structure.

Verbose mode will also print out references to additional file types, such as data_bags,
templates, included packages or pip-installed packages.

Roles and data_bags are _.json_ files, and recipes are _.rb_ files.

If no root directory is given, will default to _~/chef-repo_.

`knife deps users.json --tree` is similar, but not as detailed as I wanted.

Sample Usage and Output
-----------------------
    python role_crawl.py -d ~/chef-repo -r "role[users]" -v

    role: <users>
        recipe: <chef-handler-profiler::default>
            [include_recipe 'chef_handler']
        recipe: <yum-gd::default>
        recipe: <users::power-users>
        recipe: <sudo::default>
            [source 'sudoers.erb']
        recipe: <ssh-keys::default>
            [source "authorized_keys.erb"]
            [data_bag_item('chef-credentials', node['jenkins']['user'])]
        recipe: <opsmatic::handler>
            [include_recipe 'opsmatic::common']
        recipe: <opsmatic::agent>
            [include_recipe 'opsmatic::common']
            [include_recipe 'opsmatic::debian_public']
            [include_recipe 'opsmatic::rhel_public']
            recipe: <opsmatic_support::default>
                [source 'user-data.sh.erb']
                [source 'opsmatic_config.sh.erb']
                [source 'hosts-config.sh.erb']

    python role_crawl.py
    usage: role_crawl.py [-h] [-r ROLE] [-d DIR] [-v]
    
    Usage: specify a chef-role, and an optional root-directory. The output will be a hierarchical list of roles and recipes,
    and optionally, all external file references (templates and databags).
    
    optional arguments:
      -h, --help            show this help message and exit
      -r ROLE, --role ROLE  chef-role to crawl (required)
      -d DIR, --dir DIR     root directory where cookbooks/databags/roles are stored (optional)
      -v, --verbose         include all external references, such as templates and databags

Expected Directory Structure
----------------------------
    /cookbooks
        /recipes
            default.rb
        /templates/default
            foo.erb
    /data_bags
        /bag-name
            item.json
    /roles
        foo.json

Currently Supported:
====================

Roles external references
------------------------------
    "role[users]",
    "recipe[python]",
    "recipe[jenkins::build-dependencies]"]

Recipes external references
--------------------------------
    include_recipe 'python'
    include_recipe 'jenkins::package'
    package 'git'
    python_pip 'awscli'
    source 'aws-config.erb'
    data_bag_item('aws-credentials', node['jenkins']['bootstrap_key'])

Currently Not Supported:
========================
    Nodes
    Environments
    Run_lists inside a recipe.rb - is this possible?

To Do
-----
use root directory found in knife config

add metadata.rb depends?

colorize text?
