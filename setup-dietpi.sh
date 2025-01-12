#!/bin/bash
#
# Connect to the Raspberry Pi and install prerequisites.

set -e
cd "$(readlink -f $(dirname "${BASH_SOURCE[0]}"))"

if [ -z "$1" ]
then
    echo "usage: $0 <pi-hostname>"
    exit 2
fi

script='
# INSTALL SCRIPT TO RUN ON RASPBERRY PI

set -e

sudo apt-get install -y -y \
        python3-pip python3-setuptools python3-smbus python3-venv \
        i2c-tools libgpiod-dev python3-libgpiod

sudo adduser dietpi i2c

if [ ! -d env ]
then
  python3 -m venv env --system-site-packages
fi

source env/bin/activate
pip3 install -r requirements.txt

crontab crontab

# END OF INSTALL SCRIPT
'

for hostname in "$@"
do
    ssh $hostname sudo apt-get install -y -y less rsync
    ./push $hostname
    echo "$script" | ssh $hostname
done
