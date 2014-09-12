import urllib2
from datetime import datetime
from pyrocko.gui_util import EventMarker
from pyrocko.model import Event
from pyrocko.util import str_to_time
import locale
import re
import sys

try:
    year = sys.argv[1]
except IndexError:
    print 'USAGE: python request_Colm.py [YEAR]'
if year=='2014':
    year='temp'
    suffix = 'html'
else:
    suffix = 'htm'

url = 'http://www.uni-leipzig.de/collm/auswertung_%s.%s'%(year, suffix)
print url

usock = urllib2.urlopen(url)
data = usock.read()
usock.close()
if not year=='temp':
    data = data.split('<PRE>')[1].split('</PRE>')[0]

markers = []
for line in data.split('\n'):
    print line
    if len(line)<70:
        continue
    if not line[3].isdigit():
        continue
    print line
    if not '-2014 ' in line:
        if year=='temp':
            continue
    event_id = int(line[:4])
    date = line[5:27]
    try:
        t = datetime.strptime(date , '%d-%b-%Y %H:%M:%S.%f')
    except ValueError:
        continue
    t = (t-datetime(1970,1,1)).total_seconds()

    lat = float(line[28:34])
    lon = float(line[35:41])
    depth = float(line[43:47])
    print line[56:60]
    if year=='temp':
        mag = float(line[56:60])
    else:
        print line[60:64]
        mag = float(line[60:64])
    name = line[69::]
    e = Event(lat=lat, lon=lon, depth=depth, magnitude=mag, name=name, time=t, 
             catalog='Colm')
    print e
    m = EventMarker(e)
    markers.append(m)

EventMarker.save_markers(markers, 'event_markers_Colm%s.txt'%year)
