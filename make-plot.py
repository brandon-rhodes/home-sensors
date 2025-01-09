#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "plotly",
# ]
# ///

import plotly.graph_objects as go

from collections import defaultdict
from datetime import datetime
from glob import glob

t = []
data = defaultdict(list)

# Each line of data looks like: 2024-11-11 18:14 F=64.7 H%=63.1

for path in sorted(glob('data-basement/data-*')):
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

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=data['F'], name='Temperature (°F)'))
fig.add_trace(go.Scatter(x=t, y=data['H%'], name='Humidity (%)'))
fig.show()
