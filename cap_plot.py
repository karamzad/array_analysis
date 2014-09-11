import sys
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as num

fn = sys.argv[1]
f = open(fn, 'r')

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
    

    #if cfreq !=20.:
    #    print 'skip'
    #    continue
    #ax.scatter(baz, slow, s=20., c=sem, cmap=cmap, vmin=vmin, vmax=vmax)
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
