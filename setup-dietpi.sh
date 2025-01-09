#!/bin/bash
#
# Connect to the Raspberry Pi and install prerequisites.

set -e

if [ -z "$1" ]
then
    echo "usage: $0 <pi-hostname>"
    exit 2
fi

scp crontab recorder.py requirements.txt $1:

# install less
# dpkg-query -W -f='${Installed-Size;8}  ${Package}\n' | sort -n
# apt-cache rdepends --installed packagename  # or apt rdepends?

# apt purge firmware-atheros firmware-brcm80211 firmware-iwlwifi wpasupplicant
# After this operation, 177 MB disk space will be freed.
# apt autoremove

# After apt install of python stuff from other script:
# Recommended packages:
#   build-essential python3-dev

0:05 $ tar cf - crontab recorder.py requirements.txt | ssh pi2 tar xf -



"""
root@DietPi:~# df -h /
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       808M  696M   56M  93% /

After apt maneuvers above:

Filesystem      Size  Used Avail Use% Mounted on
/dev/root       808M  525M  226M  70% /

After pip installs:
/dev/root       808M  595M  157M  80% /


sudo raspi-config nonint do_i2c 0
^ doesn't work; but maybe not needed after initial setup?
"""

# ? firmware-misc-nonfree
