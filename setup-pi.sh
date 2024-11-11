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

ssh -t $1 <<-'EOF'

sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install \
     python3-pip python3-setuptools python3-venv \
     i2c-tools libgpiod-dev python3-libgpiod

if [ ! -d env ]
then
  python3 -m venv env --system-site-packages
fi

source env/bin/activate
pip3 install RPi.GPIO
pip3 install -r requirements.txt

sudo raspi-config nonint do_i2c 0
ls /dev/i2c*

EOF
