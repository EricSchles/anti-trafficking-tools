from io import BytesIO
from datetime import datetime
from datetime import timedelta
from geopy import geocoders
#import certifi
import pycurl
import json
import sys
import re
import pytz

#Uses pycurl to fetch a site

def query(url, username, password):
  
  output = BytesIO()

  q = pycurl.Curl()
  q.setopt(q.SSL_VERIFYPEER, 0)
  q.setopt(pycurl.POSTFIELDS, '{ "query": { "filtered": { "filter": { "term": { "url.domain": "backpage.com" } } } } }')
  q.setopt(pycurl.USERPWD, "%s:%s" % (str(username), str(password)))
  q.setopt(pycurl.URL, url)
  q.setopt(pycurl.WRITEFUNCTION, output.write)
  
  try:
    q.perform()
    status = q.getinfo(pycurl.HTTP_CODE)

    return output.getvalue(), status
  except pycurl.error as exc:
    return "Unable to reach %s (%s)" % (url, exc), '', ''


if len(sys.argv) < 3:
	print 'extractAds.py username password\n'
        sys.exit(0)

username = sys.argv[1]
password = sys.argv[2]

url = "https://els.istresearch.com:19200/memex-domains/escorts/_search?size=200&from=27595589&pretty=true"
output, status = query(url, username, password)

all_ts = []

if status == 200:
	jout = json.loads(output)
        
	for akey in jout['hits']['hits']:
            #print '_id:', akey['_id']
            if (akey.get('_source').get('extractions').get('posttime')):
                #locs = akey['_source']['extractions']['userlocation']['results'][0].encode('ascii', 'ignore')
                #print 'location:', locs
                region = akey['_source']['extractions']['region']['results'][0].encode('ascii', 'ignore')
                print 'region:', region
                g = geocoders.GoogleV3()
                timezone = g.timezone(g.geocode(region).point)
                #print timezone
                s = akey['_source']['extractions']['posttime']['results'][0]
                print 'post time:', s
                idx = s.index(",")
                day = s[:idx]
                month = ''
                months = ['January', 'February','March','April','May','June','July','August','September','October','November','December']
                for possible in months:
                    if possible in s:
                        month = possible
                        break
                year = ''
                years = ['2013','2014','2015','2016']
                for possible in years:
                    if possible in s:
                        year = possible
                        break
                p = re.compile('\d?\d\:\d\d(\sAM|\sPM)?')
                m = p.search(s)
                time = m.group()
                if time.endswith(' AM'):
                    time = time[:-3]
                else :
                    if time.endswith(' PM'):
                        time = time[:-3]
                        idx = time.index(":")
                        hour = int(time[:idx])
                        if hour != 12 : hour = hour + 12
                        time = time[idx:]
                        time = str(hour)+time
                p1 = re.compile('\s\d?\d(?!\:)')
                m1 = p1.search(s)
                date = m1.group()[1:]
                timestamp = day + ' ' + month + ' ' + date + ' ' + year + ' ' + time
                t = datetime.strptime(timestamp, "%A %B %d %Y %H:%M")
                #update to UTC timezone
                t_wts = t.replace(tzinfo=timezone)
                utc = t_wts.astimezone(pytz.utc)
                all_ts.append(utc)
                #print utc

                #print 'Post ID:', akey['_source']['url'].split('/')[-1], akey['_source']['extractions']['region']['results'][0]
                #print 'Time to extract:', akey['_source']['crawl_data']['context']['timestamp']
all_ts.sort(reverse=True)
for i in all_ts: print i
diffs = [x - y for x,y in zip(all_ts,all_ts[1:])]
diffs.sort(reverse=True)
for diff in diffs: print str(diff)
print sum(diffs, timedelta()) / len(diffs)
 
