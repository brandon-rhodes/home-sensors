import adafruit_hdc302x
import adafruit_scd4x
import adafruit_sgp40
import board
import time
from datetime import datetime, timedelta
from glob import glob

matches = len([
    path for path in glob('/proc/[1-9]*/cmdline')
    if 'python\000recorder.py' in open(path).read()
])
if matches > 1:
    exit('Error: recorder.py already running')

zero = timedelta()

i2c = board.I2C()                 # uses board.SCL and board.SDA
errors = RuntimeError, ValueError # laptop versus Raspberry Pi

try:
    hdc302x = adafruit_hdc302x.HDC302x(i2c)
except errors:
    hdc302x = None

try:
    scd4x = adafruit_scd4x.SCD4X(i2c)
except errors:
    scd4x = None
else:
    print('SCD4X serial number:', ' '.join(hex(i) for i in scd4x.serial_number))
    scd4x.start_periodic_measurement()

try:
    sgp = adafruit_sgp40.SGP40(i2c)
except errors:
    sgp = None

#delay = timedelta(seconds=2)
delay = timedelta(minutes=1)

def main():
    dt = datetime.now()
    dt = dt.replace(second=0, microsecond=0)
    dt += delay * 2
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
    if hdc302x is not None:
        yield 'F', '%.1f' % celsius_to_fahrenheit(hdc302x.temperature)
        yield 'H%', '%.1f' % hdc302x.relative_humidity
    if scd4x is not None and scd4x.data_ready:
        yield 'CO2_ppm', '%d' % scd4x.CO2
        yield 'F', '%.1f' % celsius_to_fahrenheit(scd4x.temperature)
        yield 'H%', '%.1f' % scd4x.relative_humidity
    if sgp is not None:
        yield 'voc_raw', str(sgp.raw)

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
