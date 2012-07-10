autodc
======

**autodc** is a small script used to automatize the transfer of digital images
from a digital camera into a specified directory.
It is made of two files:
 * a rule file for [udev](http://wiki.debian.org/udev) ;
 * a [Python](http://python.org) script to be launched when a camera is plugged.

Configuration is kinda specific to my way of doing on my Linux box. I use:
 * [gphoto](http://gphoto.org) to get the pictures from the camera ;
 * [Fabric](http://docs.fabfile.org) to deploy both files ;
 * bootstrap, a personal treat to create a
 [virtualenv](http://www.virtualenv.org) containing all you need.


Install
-------
Clone the repository and just type:

    source bootstrap

to create the virtualenv, get the dependencies and start being able to use
autodc. Then, configure the `fabfile.py` file and deploy the code over the
machines you configure it to with:

    fab deploy


Configuration
-------------
You need to specify in the `fabfile.py` file what machines you want **autodc**
to be usable from. There's already one configuration to see as an example:

    CONFIGS = [
        {'host':'192.168.0.1',
         'user':'user',
         'directory':'/home/user/images/Incoming/'
        },
        {'host':'192.168.0.2',
         'user':'gitmaster',
         'directory':'/home/gitmaster/pictures/Incoming/'
        },
    ]

For every machine you have, just set the local IP address, the corresponding
user name and the directory you want the pictures to be transferred in.
BE CAREFUL to specify a directory that is into the user's `/home` directory.


Supported cameras
-----------------
For the moment, only the few cameras I own are supported. If you want yours
to be, just add a rule in the `100-autodc.rules` file, specifying the
`ATTRS{idVendor}` and `ATTRS{idProduct}` values. You can find them for your own
device with the command `lsusb` while it is plugged.

Some me your udev values, I'll add them to the file for the world.
Next step will be to find some values in a file like `/lib/udev/rules.d/60-libgphoto2-2.rules`.
