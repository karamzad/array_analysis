#!/usr/bin/python 

import sys
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as num
from pyrocko.gui_util import Marker
from pyrocko import util
from pyrocko.gf import seismosizer

# first argument is the filename of CAP output, second argument the filename
# of file containing event markers

fn = sys.argv[1]
markers = Marker.load_markers(sys.argv[2])
f = open(fn, 'r')
flist = fn.split('.')[0]
print 'filename ',fn
event_times = ['2013-01-12 08:54:19.000',
'2013-01-14 03:34:08.500',
'2013-03-11 01:26:45.100',
'2013-04-22 22:46:00.300',
'2013-04-23 00:28:30.300',
'2013-04-23 02:44:05.100',
'2013-04-30 19:03:06.800',
'2013-07-04 12:29:47.600'] #Is there a second event in here??

flists = ['2013-01-12',
          '2013-01-14',
          '2013-03-11',
          '2013-04-22',
          '2013-04-23-00',
          '2013-04-23-02',
          '2013-04-30',
          '2013-07-04']
mapping = dict(zip(flists, event_times))

event_time = mapping[flist]
print 'event time ', event_time
for em in markers:
    if em.tmin==util.str_to_time(event_time):
        event = em._event
        source = seismosizer.Source.from_pyrocko_event(event)
        break

# calculate theoretical azimut and backazimuth  
center_array_target = seismosizer.Target(lat=50.241611, lon=12.327766)
distance = center_array_target.distance_to(source)
azibazi = center_array_target.azibazi_to(source)
print 'Azimuth: %s, Backazimuth: %s' %(azibazi)

cmap = plt.cm.jet
vmin = 0.
vmax =0.6
def make_array(f):
    #ORDER:
    # t, cfreq, slow, baz, mathpi, sem, beampow, avgsem, avgsemtheo, obstheo 
    data_array = []
    for line in f.readlines():

        if line[0] == ('#'):
            continue
        data = line.split()
        data = [float(v) for v in data]
        data_array.append(data)
    data_array = num.array(data_array)
    return data_array
    

d = make_array(f)
cfreq = d.T[1]
cfreqs = num.unique(cfreq)
num_subplots = len(cfreqs)
f, axs = plt.subplots(1, num_subplots, subplot_kw=dict(polar=True))
f2, axlin = plt.subplots(2,1)
axs2 = axlin[0]
axs3 = axs2.twinx()
axs4 = axlin[1]
#f4, axs4 = plt.subplots()


theta_max = 0.3
# loop over center frequencies
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
    axs2.set_ylabel('Semblance')
    axs3.plot(t, beamp, label=cf)
    axs3.set_ylabel('Beam power')
    axs2.set_xlabel("time [s]")

    # plot bazi over time
    axs4.plot(t, baz)
    axs4.set_xlabel('time [s]')
    axs4.set_ylabel('back azimuth [deg]')

    # Draw polar bazi, slowness and semblance plot
    ax = axs[i]
    ax.scatter(baz*num.pi/180., 
               slo, 
               s=32, 
               c=sem, 
               cmap=cmap,
               vmin=vmin,
               vmax=vmax)
      
    # Add arrow indicting azimuth of maximum  
    i_sem_max = num.where(sem==max(sem))[0][0]
    ax.arrow(0,0, baz[i_sem_max]/180*num.pi, theta_max, edgecolor='r',
            label=r'$\theta_[theo]$') 
    
    # Add arrow indicting theoretical direction
    ax.arrow(0,0, azibazi[0]/180*num.pi, theta_max,
            label='FK')
    # Turn plot so that North is up
    ax.set_theta_zero_location('N')

    # Use negative mathematical (counter clockwise direction)
    ax.set_theta_direction(-1)

    # limit slowness range
    ax.set_ylim([0., theta_max])
    ax.set_title("Center Frequency %s Hz"%cf, fontsize=14)

f2.subplots_adjust(wspace=0., hspace=0.)
ax.legend(bbox_to_anchor=(0,0,1,1), bbox_transform=f.transFigure)
axs2.legend(title=r'$f_c [Hz]$')
fnnew = fn.split()[0]
fn_new_lin = fnnew+'_lin.pdf'
fn_new_pol = fnnew+'_pol.pdf'
plt.show()

f.savefig(fn_new_pol)
f2.savefig(fn_new_lin)
