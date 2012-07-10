#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Deployment of autodc. """

# directories should be into user's home
CONFIGS = [
    {'host':'192.168.0.1',
     'user':'user',
     'directory':'/home/user/images/Incoming/'
    },
]


# globals
BINDIR = '~/bin'
ETCDIR = '/etc/udev/rules.d'
RULES_FILE = '100-autodc.rules'
SCRIPT_FILE = 'autodc.py'


# system
import tempfile
from string import Template
from os.path import join
# fabric
from fabric.api import cd, settings
from fabric.operations import put


def deploy():
    """ Deploys both '100-autodc.rules' and 'autodc.py' files
        to configurations defined in global variables. """
    for conf in CONFIGS:
        # udev file
        with settings( host_string=conf['host'], user='root' ):
            script_path = join('/home', conf['user'], SCRIPT_FILE)
            substitute = dict(script=script_path)
            with tempfile.TemporaryFile() as rules_temp:
                # write temp files from template
                with open(RULES_FILE, 'r') as line:
                    template_line = Template(line.read())
                    new_line = template_line.safe_substitute(substitute)
                    rules_temp.write(new_line)

                #put temp files on remote machine
                with cd(ETCDIR):
                    put(rules_temp, RULES_FILE)

        # script file
        with settings( host_string=conf['host'], user=conf['user'] ):
            substitute = dict(autodc_directory=conf['directory'])
            with tempfile.TemporaryFile() as script_temp:
                # write temp files from template
                with open(SCRIPT_FILE, 'r') as line:
                    template_line = Template(line.read())
                    new_line = template_line.safe_substitute(substitute)
                    script_temp.write(new_line)

                # put temp files on remote machine
                with cd(BINDIR):
                    put(script_temp, SCRIPT_FILE, mode=0755)

