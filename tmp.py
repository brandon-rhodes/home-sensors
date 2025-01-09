import hid
print(0x04D8, 0x00DD)
print(hid.enumerate())
device = hid.device()
device.open(0x04D8, 0x00DD)
