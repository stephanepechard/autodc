autodc
======

**autodc** is a small script used to automatize the transfer
of digital pictures from a digital camera into a specified directory.
It is made of two files:
 * a rule file for [udev](http://wiki.debian.org/udev) ;
 * a [Python](http://python.org) script to be launched when a camera is plugged.

Configuration is kinda specific to my way of doing on my Linux box. I use:
 * [gphoto](http://gphoto.org) to get the pictures from the camera ;
 * [Fabric](http://docs.fabfile.org) to deploy both files ;
 * a personal script to create a
 [virtualenv](http://www.virtualenv.org) containing all we need to use **autodc**.


Install
-------
Clone the repository and just type:

    source bootstrap

to create and enter the virtualenv, get the dependencies and start
being able to use **autodc**. If you just need to install it
on the current machine, type:

    mkdir -p ~/bin && cp autodc.py ~/bin && sudo cp 100-autodc.rules /etc/udev/rules.d/

If you need to deploy the files over many computers, configure the `fabfile.py`
file and deploy the code over the machines you configure it to with:

    fab deploy

When you need to deploy the files again at a later point, don't forget
to enter the virtual environment.


Configuration
-------------
You need to specify in the `fabfile.py` file what machines you want **autodc**
to be usable from. There's already one configuration to see as an example,
add our own other configurations like this:

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

For every machine you have, set the local IP address, the corresponding
user name and the directory you want the pictures to be transferred in.
BE CAREFUL to specify a directory that is into the user's `/home` directory.


Supported cameras
-----------------
**1285** camera identities were taken from the file
`/lib/udev/rules.d/60-libgphoto2-2.rules` of
[Debian](http://debian.org) package 
[libgphoto2](http://packages.debian.org/wheezy/libgphoto2-2).
The only drawback is not to be able to know the exact camera model
corresponding this list.

If you need some more identities, feel free to propose an addition.
You can find it with the command `lsusb` while your device is plugged.


Limitations
-----------
Two main limitations are known and unlikely to be corrected in any way.
The first one is that pictures are not renamed, which is convenient 
in dedicated softwares when pictures are imported. The used name is
then the name given by the digital camera. Images are separated in
directories named after the camera model. But if you plug different
cameras of the same model, it may happen that your first pictures
are overwritten. This would be a pity. So always consider the incoming 
directory as a temporary storage before your own classification.

The second limitation is that no information is kept about
what pictures have already been transfered, so if you plug
a camera twice, pictures are transfered again and overwritten.
You know it, you handle it.
