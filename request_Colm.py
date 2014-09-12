import urllib2
from datetime import datetime
from pyrocko.gui_util import EventMarker
from pyrocko.model import Event
from pyrocko.util import str_to_time
import locale
import re
#locale.setlocale(locale.LC_ALL, 'de_DE')

year = 2014
#url = 'http://www.uni-leipzig.de/collm/auswertung_%s.htm'%year
url = 'http://www.uni-leipzig.de/collm/auswertung_temp.html'

usock = urllib2.urlopen(url)
data = usock.read()
usock.close()
if not year==2014:
    data = data.split('<PRE>')[1].split('</PRE>')[0]
#else:
#    data = data.rsplit('<PRE>')[1].split('</PRE>')[0]
#    print data

markers = []
for line in data.split('\n'):
    if len(line)<70:
        continue
    if not line[3].isdigit():
        continue
    print line
    #print line
    print line
    if not '-2014 ' in line:
        continue
    event_id = int(line[:4])
    date = line[5:27]
    try:
        t = datetime.strptime(date , '%d-%b-%Y %H:%M:%S.%f')
    except ValueError:
        continue
    t = (t-datetime(1970,1,1)).total_seconds()
    print t

    lat = float(line[28:34])
    lon = float(line[35:41])
    depth = float(line[43:47])
    print line[56:60]
    mag = float(line[56:60])
    name = line[69::]
    e = Event(lat=lat, lon=lon, depth=depth, magnitude=mag, name=name, time=t, 
             catalog='Colm')
    print e
    m = EventMarker(e)
    markers.append(m)

EventMarker.save_markers(markers, 'event_markers_Colm%s.txt'%year)
