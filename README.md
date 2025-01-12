# home-sensors
Scripts to collect home environment data with a Raspberry Pi

Of the two Adafruit sensors boards I am trying out, initial tests
suggest that the ‘scd4x’ board has 1.5°F lower temperature and around 2%
higher humidity than the ‘hdc302x’ board.

# Installing DietPi on the Raspberry Pi

I downloaded DietPi for the ‘Raspberry Pi 1/Zero (1)’, inserted the Pi’s
SD card into the laptop’s SD slot, and then:

```
xzcat ~/Downloads/DietPi_RPi-ARMv6-Bookworm.img.xz | sudo dd of=/dev/mmcblk0
```

Then I mounted the boot partition, and edited `dietpi.txt` to set:

```
AUTO_SETUP_NET_HOSTNAME=example
AUTO_SETUP_SSH_PUBKEY=ssh-rsa ...
AUTO_SETUP_AUTOMATED=1
SOFTWARE_DISABLE_SSH_PASSWORD_LOGINS=1
```

And I made one change to `config.txt`:

```
dtparam=i2c_arm=on
```

Alas — after inserting the SD card into the Raspberry Pi and booting it,
I never saw a new SSH server appear on the network.  So I hooked the Pi
up to a monitor and keyboard and saw that it was waiting at its initial
`Login:` prompt, which apparently can’t be skipped to make the install
truly headless.  (I guess that’s why the comment in `dietpi.txt` says
‘On first login’, a subtlety I missed on first reading.)  So I logged in
as `root`, and the automated install then proceeded.

Then, I added the new device’s IP address to my `~/.ssh/config`:

```
Host example
  Hostname 192.168.1.38
  User dietpi
```

And then I could run the setup script in this repository:

```
$ ./setup-dietpi.sh example
```

After SSH’ing into the Raspberry Pi, I could successfully run:

    ./env/bin/python recorder.py

— and see the I2C devices detected successfully.  So I finished the
setup with:

    crontab crontab

— and the environment logging has been running ever since.

# Special maneuvers for a small SD card

For one of my Raspberry Pi’s, I could only find a 2GB SD card, which
just barely fit the initial DietPi image.  So I proceeded only a little
way into the setup before getting a shell prompt and asking how I could
free up space on the filesystem to install Python.  This listed the
installed packages by installed footprint:

    dpkg-query -W -f='${Installed-Size;8}  ${Package}\n' | sort -n

A very large amount of space was taken up with Wifi firmware, which I
didn’t need since my old Raspberry Pi’s don’t even have Wifi.  Thus:

    apt purge firmware-atheros firmware-brcm80211 firmware-iwlwifi wpasupplicant

The result was that free space on the filesystem shown by `df -h /`
increased from 56M to 226M, which was enough to proceed with setup and
get the environment recorder running.  After installing Python and other
dependencies, free space was still a comfortable 152M.

For my own future reference, these two commands were helpful as I did
the investigation that resulted in the above `purge` command:

    apt-cache rdepends --installed packagename
    apt autoremove
