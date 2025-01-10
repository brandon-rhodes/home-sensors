#
# SGP40 Air Quality Sensor: https://www.adafruit.com/product/4829

import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from glob import glob

fmt = "%Y-%m-%d %H:%M:%S"
zero = timedelta()
print('Home Sensor Recorder starting up at', datetime.now().strftime(fmt))

def try_reading(path):          # avoid race condition where file disappears
    try:
        return open(path).read()
    except FileNotFoundError:
        return ''

matches = len([
    path for path in glob('/proc/[1-9]*/cmdline')
    if 'python\000recorder.py' in try_reading(path)
])
if matches > 1:
    exit('Error: recorder.py already running')

if subprocess.call('lsusb | grep -q MCP2221', shell=True) == 0:
    print('MCP2221 detected on USB bus')
    os.environ['BLINKA_MCP2221'] = '1'
else:
    print('I2C bus not detected on USB; using built-in I2C')

# These imports must be delayed until BLINKA_MCP2221 is set:

import adafruit_hdc302x
import adafruit_scd4x
import adafruit_sgp40
import board

print('Board:', board.detector.board.id)
print('Chip:', board.detector.chip.id)

i2c = board.I2C()                 # uses board.SCL and board.SDA
print('I2C scan:', ' '.join(str(n) for n in sorted(i2c.scan())))

errors = RuntimeError, ValueError # laptop versus Raspberry Pi

try:
    hdc302x = adafruit_hdc302x.HDC302x(i2c)
except errors:
    hdc302x = None
print('HDC302x:', hdc302x)

try:
    scd4x = adafruit_scd4x.SCD4X(i2c)
except errors:
    scd4x = None
    print('SCD4X:', scd4x)
else:
    print('SCD4X serial number:', ' '.join(hex(i) for i in scd4x.serial_number))
    scd4x.start_periodic_measurement()

try:
    sgp = adafruit_sgp40.SGP40(i2c)
except errors:
    sgp = None
print('SGP40:', sgp)

if len(sys.argv) > 1:            # add argument for quicker debug startup
    delay = timedelta(seconds=1)
else:
    delay = timedelta(minutes=1)

def main():
    dt = datetime.now()
    dt = dt.replace(second=0, microsecond=0)
    dt += delay * 2  # give sensors at least one full minute to warm up
    while True:
        wait_until(dt)
        measurements = list(make_measurements())
        record(dt, measurements)
        dt += delay

def wait_until(dt):
    now = datetime.now()
    delay = dt - now
    if delay > zero:
        time.sleep(delay.total_seconds())

def make_measurements():
    C = None
    H = None
    if hdc302x is not None:
        C = hdc302x.temperature
        H = hdc302x.relative_humidity
        yield 'F', '%.1f' % celsius_to_fahrenheit(C)
        yield 'H%', '%.1f' % H
    if scd4x is not None and scd4x.data_ready:
        C = scd4x.temperature
        H = scd4x.relative_humidity
        yield 'CO2_ppm', '%d' % scd4x.CO2
        yield 'F', '%.1f' % celsius_to_fahrenheit(C)
        yield 'H%', '%.1f' % H
    if sgp is not None:
        if (C is not None) and (H is not None):
            raw = sgp.measure_raw(temperature=C, relative_humidity=H)
        else:
            raw = sgp.raw
        yield 'voc_raw', str(raw)

def celsius_to_fahrenheit(celsius):
    """Converts Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def record(dt, measurements):
    text = f'{dt:%Y-%m-%d %H:%M}'
    for key, value in measurements:
        text += f' {key}={value}'
    filename = f'data-{dt:%Y-%m-%d}'
    print(text)
    text += '\n'
    with open(filename, 'a') as f:
        f.write(text)

if __name__ == '__main__':
    main()
