#!/usr/bin/env -S uv run --script

# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "numpy",
#     "plotly",
# ]
# ///

import argparse
import plotly.graph_objects as go
import numpy as np
import sys

from collections import defaultdict
from datetime import datetime, timedelta
from glob import glob

parser = argparse.ArgumentParser()
parser.add_argument('source', choices=('attic', 'basement', 'office'))
parser.add_argument('data', choices=('th', 'co2', 'voc'))
args = parser.parse_args()

#pattern = 'data-basement/data-*'
pattern = f'data-{args.source}/data-*'

t = []
data = defaultdict(list)

# Each line of data looks like: 2024-11-11 18:14 F=64.7 H%=63.1

for path in sorted(glob(pattern)):
    print(path)
    for line in open(path):
        line = line.replace('\000', '')  # how did nulls get in there?
        if 'F=-49.0' in line:
            continue

        # if line < '2025-03-11 05':
        #     continue
        # if line > '2025-04-01 05':
        #     continue
        dt = datetime.strptime(line[:16], '%Y-%m-%d %H:%M')
        t.append(dt)

        for field in line[16:].split():
            name, value = field.split('=')
            value = float(value)
            data[name].append(value)

data = dict(data)

# Eastern Time Zone.
zone = timedelta(hours=-5)
t = [i + zone for i in t]

one_minute = timedelta(minutes=1)

def segments(t):  # do this in talk? orig, built two lists for each seg
    i = 0
    tprev = t[0]
    for j, ti in enumerate(t):
        if ti - tprev > one_minute:
            yield i, j
            i = j
        tprev = ti
    yield i, j

if args.data == 'th':
    fig = go.Figure()
    add = fig.add_trace
    for i, j in segments(t):
        tij = t[i:j]
        add(go.Scatter(x=tij, y=data['F'][i:j], line_color='blue',
                       name='°F'))
                       #name='Temperature (°F)'))
        # add(go.Scatter(x=tij, y=data['H%'][i:j], line_color='red',
        #                name='%H'))
        #                #name='Humidity (%)'))
    fig.show()

elif args.data == 'co2':

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=data['CO2_ppm'], name='CO2 (ppm)'))
    fig.show()

elif args.data == 'voc':

    clip_upper = min
    data = [clip_upper(33e3 - datum, 5e3) for datum in data['voc_raw']]

    def moving_average(a, n):
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n

    #data = moving_average(data, 120)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=data, name='VOC raw'))
    fig.show()

# from adafruit_sgp40 import SGP40

# class SGP40_offline(SGP40):
#     def __init__(self):
#         self._voc_algorithm = None
#     def set_next_raw_measurement(self, value):
#         self.datum = value
#     def measure_raw(self, temperature, relative_humidity):
#         return self.datum

# def compute_voc_index():
#     harness = SGP40_offline()
#     series = []
#     sixty = range(60)
#     for item in data['voc_raw']:
#         harness.set_next_raw_measurement(item)
#         for i in sixty:
#             voc = harness.measure_index(None, None)
#             series.append(voc)
#     return series

# voc_index = compute_voc_index()

# import csv
# with open('data-office/voc.csv') as f:
#     rows = list(csv.reader(f))
# print(rows[:10])
# strptime = datetime.strptime
# rows = [
#     (strptime(row[0], '%Y-%m-%d %H:%M:%S'), float(row[1]))
#     for row in rows[1:]
# ]
# print(rows[:10])
# t, voc = list(zip(*rows))
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=t, y=voc, name='VOC index'))
# fig.show()

# import csv
# voc = [int(word) for word in open('voc.out').read().split()]
# print(voc[:10])
# fig = go.Figure()
# fig.add_trace(go.Scatter(y=voc, name='VOC index'))
# fig.show()
