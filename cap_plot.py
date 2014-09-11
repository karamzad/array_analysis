import sys
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as num
from pyrocko.gui_util import Marker
from pyrocko import util
from pyrocko.gf import seismosizer

fn = sys.argv[1]
f = open(fn, 'r')

markers = Marker.load_markers(sys.argv[2])
event_time = '2013-03-11 01:26:45.100'

for em in markers:
    if em.tmin==util.str_to_time(event_time):
        event = em._event
        source = seismosizer.Source.from_pyrocko_event(event)
        break

# calculate theoretical azimut and backazimuth  
center_array_target = seismosizer.Target(lat=50.2417175, lon=12.328385875)
distance = center_array_target.distance_to(source)
azibazi = center_array_target.azibazi_to(source)

cmap = plt.cm.jet
vmin = 0.
vmax =0.6
def make_array(f):
    data_array = []
    for line in f.readlines():

        if line[0] == ('#'):
            continue
        data = line.split()
        data = [float(v) for v in data]
        data_array.append(data)
    data_array = num.array(data_array)
    return data_array
    #t, cfreq, slow, baz, mathpi, sem, beampow, avgsem, avgsemtheo, obstheo = data
    

d = make_array(f)
cfreq = d.T[1]
cfreqs = num.unique(cfreq)
num_subplots = len(cfreqs)
f, axs = plt.subplots(1, num_subplots, subplot_kw=dict(polar=True))
f2, axs2 = plt.subplots()
for i,cf in enumerate(cfreqs):
    ind = num.where(d.T==cf)[1]
    d_T  = d.T
    t = d_T[0][ind]
    baz = d_T[3][ind]
    slo = d_T[2][ind]
    sem = d_T[5][ind]
    beamp = d_T[6][ind]

    vmin = min(sem)
    vmax = max(sem)
    axs2.plot(t, sem, label=cf)
    axs2.plot(t, beamp, label=cf)
    axs[i].scatter(baz, slo, s=30, c=sem, cmap=cmap, vmin=vmin, vmax=vmax, picker=True)

axs2.legend()

plt.show()
