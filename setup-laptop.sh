
umask 022

# See https://unix.stackexchange.com/questions/85379/dev-hidraw-read-permissions
#
# Debugged some with:
#
# udevadm control --log-priority=debug
# journalctl -f
# udevadm control --log-priority=info

cat > /etc/udev/rules.d/99-mcp2221.rules <<'EOF'
SUBSYSTEM=="usb", ATTRS{idVendor}=="04d8", ATTR{idProduct}=="00dd", MODE="0666", GROUP="plugdev"
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0660", GROUP="plugdev"
EOF
