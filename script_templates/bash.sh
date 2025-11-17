#!/usr/bin/bash

# SETUP ---------------------------------------
# Make temp dir for the e2tools, so that we do not leave any artifacts afterwards
mkdir /tmp/e2
cd /tmp/e2

# Download the e2tools to manipulate the .img file
apt download e2tools
dpkg-deb -x e2tools_*.deb .
# SETUP END -----------------------------------


# Use tools (in-place, no install)
./usr/bin/e2mkdir disk.img:/test
./usr/bin/e2cp myfile.txt disk.img:/test/file.txt

# create 16MB image file
dd if=/dev/null of=test.img bs=1 count=1 seek=16M

# create filesystem inside image file
mkfs.ext2 -F test.img

# create directory foo in root directory of filesystem image
e2mkdir test.img:/foo

# look into root directory of filesystem image
e2ls -l test.img:

# copy README.md into foo dir
e2cp README.md test.img:/foo

# look what is inside the foo dir
e2ls -l test.img:/foo

# remove file again
e2rm test.img:/foo/README.md






# CLEAN UP ---------------------------------------
cd /
rm -rf /tmp/e2
# CLEAN UP END -----------------------------------
