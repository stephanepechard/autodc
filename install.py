#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Local installation script for autodc. """

__version__ = '0.2'

# system
import os
import re
import subprocess
import sys
from string import Template


def username_from_homepath(path):
    """ Find the username from any user's home path. """
    username = None
    matched = re.match(r"/home/(\w+)/(.*)", path)
    if matched:
        username = matched.group(1)
    return username


def create_templated_file(target, template, substitutes):
    """ Create a file from a template, based on a substitutes dictionary. """
    creation = False
    try:
        with open(target, 'w') as dst:
            with open(template, 'r') as src:
                line = Template(src.read())
                dst.write(line.safe_substitute(substitutes))
        creation = True
    except IOError:
        creation = False

    return creation


def create_dir(directory):
    """ Create a directory on the user file system. """
    if not os.path.isdir(directory):
        os.mkdir(directory, 0755)


# ask directory to install script in (default: ~/bin)
found_dir = os.path.join(os.environ['HOME'], 'bin')
asked_dir = raw_input("[INPUT] Directory to install autodc script in [{0}] "
                      .format(found_dir))
bin_dir = found_dir if not asked_dir else asked_dir
create_dir(bin_dir)  # create it if it does not exist already

# ask directory to images into (default: ~/Images)
image_dir = os.path.join(os.environ['HOME'], 'Images')
asked_dir = raw_input("[INPUT] Directory to put images in [{0}] ".format(image_dir))
images_dir = image_dir if not asked_dir else asked_dir
create_dir(images_dir)  # create it if it does not exist already

# create rules file
rules_target = '/tmp/100-autodc.rules'
source = os.path.join(os.path.dirname(__file__), '100-autodc.template')
script_path = os.path.join(bin_dir, 'autodc.py')
subs = {'script': script_path}
if not create_templated_file(rules_target, source, subs):
    sys.exit('[ERROR] Failed to create rules file!')

# create and copy user script
source = os.path.join(os.path.dirname(__file__), 'autodc.template')
subs = {'autodc_directory': images_dir, 'version': __version__}
if not create_templated_file(script_path, source, subs):
    sys.exit('[ERROR] Failed to create script file!')
os.chmod(script_path, 0755)  # make it executable

# copy rules file and reload udev (needs root access)
print("[INFO] Root access is needed to copy a file in the system.")
ret = subprocess.call(['sudo', 'mv', rules_target, '/etc/udev/rules.d/'])
ret = subprocess.call(['sudo', '/etc/init.d/udev', 'reload'])
