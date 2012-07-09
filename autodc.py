#!/usr/bin/python
# -*- coding: utf-8 -*-
""" autodc.py Python script.
    Created by Stéphane Péchard on 2012-06-24. """

# system
import dbus
import logging
import os
import re
import sys
import time
from datetime import datetime
from pwd import getpwnam
from subprocess import Popen, PIPE, CalledProcessError, check_output


def username_from_homepath(path):
    """ Find the username from a user's home path. """
    username = None
    matched = re.match(r"/home/(\w+)/(.*)", path)
    if matched:
        username = matched.group(1)
    return username


def setuid_from_homepath(path):
    """ Change the uid of the process to the username of the path. """
    username = username_from_homepath(path)
    uid = getpwnam(username).pw_uid
    os.setuid(uid)


def log_and_exit(message):
    """ Own logging print in case of error. """
    logging.error(message)
    sys.exit("[ERROR] {0} ".format(message))


def main():
    """ Main function. """
    setuid_from_homepath(os.path.abspath( __file__ ))

    # start logging
    print("[INFO] getDCcontent.py version 0.1,"
                                    " created by Stéphane Péchard.")
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        filename='/tmp/dc_content_{0}.log'
                                 .format(datetime.now().isoformat()),
                        level=logging.INFO)
    logging.info('Start')


    # find which camera is plugged
    try:
        cmd = Popen(['gphoto2', '--auto-detect'], stdout=PIPE)
        stdoutdata = cmd.communicate()
    except OSError:
        log_and_exit("gphoto2 was not found, please install it!")

    camera_name = None
    for line in stdoutdata[0].split('\n'):
        usb_string = 'usb:'
        if usb_string in line:
            index = line.index(usb_string)
            camera_name = line[:index].rstrip()

    if not camera_name:
        log_and_exit("Camera name can't be found.")

    logging.info("Found '{0}' connected.".format(camera_name))


    # create the directory and cd there
    dir_name = None #$autodc_directory + camera_name
    if not os.path.isdir(dir_name):
        try:
            os.makedirs(dir_name)
            logging.info("Created '{0}' directory.".format(dir_name))
        except OSError:
            log_and_exit("Can't create directory.")
    os.chdir(dir_name)


    # get the files
    try:
        check_output(['gphoto2', '--get-all-files', '--quiet'])
    except OSError:
        log_and_exit("gphoto2 was not found, please install it!")
    except CalledProcessError:
        log_and_exit("gphoto2 did not finish well, sorry!")


    # notify the user
    try:
        knotify = dbus.SessionBus().get_object('org.kde.knotify',
                                               '/Notify')
        knid = knotify.event('warning', 'kde', [],
                             'Auto copy',
                             'Images from {0} have been copied!'
                             .format(camera_name),
                             [], [], 0, 16,
                             dbus_interface="org.kde.KNotify")
        time.sleep(16)
        knotify.closeNotification(knid)
    except dbus.exceptions.DBusException:
        log_and_exit("notification couldn't be launched...")


    # terminate
    logging.info("Done!")


if __name__ == '__main__':
    main()

