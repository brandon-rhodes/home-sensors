#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "adafruit-circuitpython-sgp40",
#     "plotly",
# ]
# ///

import plotly.graph_objects as go

from collections import defaultdict
from datetime import datetime
from glob import glob

#pattern = 'data-basement/data-*'
pattern = 'data-office/data-*'

t = []
data = defaultdict(list)

# Each line of data looks like: 2024-11-11 18:14 F=64.7 H%=63.1

for path in sorted(glob(pattern)):
    print(path)
    for line in open(path):
        line = line.replace('\000', '')  # how did nulls get in there?
        if 'F=-49.0' in line:
            continue

        dt = datetime.strptime(line[:16], '%Y-%m-%d %H:%M')
        t.append(dt)

        for field in line[16:].split():
            name, value = field.split('=')
            value = float(value)
            data[name].append(value)

data = dict(data)

# fig = go.Figure()
# fig.add_trace(go.Scatter(x=t, y=data['F'], name='Temperature (°F)'))
# fig.add_trace(go.Scatter(x=t, y=data['H%'], name='Humidity (%)'))
# fig.show()

# fig = go.Figure()
# fig.add_trace(go.Scatter(x=t, y=data['CO2_ppm'], name='VOC_raw'))
# fig.show()

# fig = go.Figure()
# fig.add_trace(go.Scatter(x=t, y=data['voc_raw'], name='VOC raw'))
# fig.show()

from adafruit_sgp40 import SGP40

class SGP40_offline(SGP40):
    def __init__(self):
        self._voc_algorithm = None
    def set_next_raw_measurement(self, value):
        self.datum = value
    def measure_raw(self, temperature, relative_humidity):
        return self.datum

def compute_voc_index():
    harness = SGP40_offline()
    series = []
    for item in data['voc_raw']:
        harness.set_next_raw_measurement(item)
        voc = harness.measure_index(None, None)
        series.append(voc)
    return series

voc_index = compute_voc_index()

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=voc_index, name='VOC index'))
fig.show()
