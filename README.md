[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/stephanepechard/autodc/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

autodc
======

**autodc** is a small script used to automatize the transfer of digital
pictures from a digital camera into a specified user directory.
It is made of two files:
 * a rule file for [udev](http://wiki.debian.org/udev) ;
 * a [Python](http://python.org) script to be launched when a camera is plugged.

I use [gphoto](http://gphoto.org) to get the pictures from the camera. You
need it too to make good use of autodc.


Install
-------
Clone the repository and just launch the installer:

    python install.py

It will ask you:
 * the directory where to put the script, default is: `~/bin` ;
 * the directory where images from your digital cameras will be copied,
   default is: `~/Images` ;
 * root access (via sudo) to copy the udev rules file in the system tree and
   to reload udev.


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
Two main limitations are known and unlikely to be fixed in any way.
The first one is that pictures are not renamed, which is convenient 
in dedicated softwares when pictures are imported. The used name is
then the name given by the digital camera. Images are separated in
directories named after the camera model. But if you plug different
cameras of the same model, it may happen that your first pictures
are overwritten. This would be a pity. So always consider the incoming 
directory as a **temporary storage** before your own classification.

The second limitation is that no information is kept about
what pictures have already been transfered, so if you plug
a camera twice, pictures are transfered again and overwritten.
You know it, you handle it.
