from lxml import html
import wikipedia
import requests
import re
import sys
import json
from geopy.geocoders import Nominatim
#import geocoder

geolocator = Nominatim()
url_table = {
	'cus'	:	'http://bikeandbuild.org/route/central-united-states/',
	'c2c'	:	'http://bikeandbuild.org/route/connecticut-to-california/',
	'me2sb'	:	'http://bikeandbuild.org/route/maine-to-santa-barbara/',
	'nc2sd'	:	'http://bikeandbuild.org/route/north-carolina-to-san-diego/',
	'nus'	:	'http://bikeandbuild.org/route/northern-united-states/',
	'p2s'	:	'http://bikeandbuild.org/route/providence-to-seattle/',
	'sc2sc'	:	'http://bikeandbuild.org/route/south-carolina-to-santa-cruz/',
	'sus'	:	'http://bikeandbuild.org/route/southern-united-states/',
	'cd'	:	'http://bikeandbuild.org/route/coastal-drift/',
	'dw'	:	'http://bikeandbuild.org/route/drift-west/',
	'cwm'	:	'http://bikeandbuild.org/route/cwm/' }
route = raw_input("which route?!? ")
if not url_table.has_key(route):
	print "wtf is that route?!?"
	sys.exit()
page = requests.get(url_table.get(route))
tree = html.fromstring(page.content)

#This will create a list of dates:
#dates = tree.xpath('//div[@title="buyer-name"]/text()')
#This will create a list of places:
places = tree.xpath('//p[@class="loc-loc"]/text()')
#for place in places:
#	place = re.sub('\n','',place)
#	place = re.sub('\t','',place)
places = [ws.replace('\n', '') for ws in places]
places = [ws.replace('\t', '') for ws in places]
places = [ x for x in places if "Build Day" not in x ]
places = [ x for x in places if "Day Off" not in x ]

#print 'places: ', places
#for place in places:
#	try:
#		print wikipedia.summary(place, sentences=1)
#	except wikipedia.exceptions.DisambiguationError as e:
#		print e.options
dict_list = []
for place in places:
	info = {
		"name":		place,
		"lat":		geolocator.geocode(place).latitude,
		"lon":		geolocator.geocode(place).longitude
#		"lat":		geocoder.google(place).lat,
#		"lon":		geocoder.google(place).lng
	}
	if info not in dict_list:
		dict_list.append(info)

print dict_list

# formatting: {"KMAE":[-120.12,36.98,"",[]],
#print json.dumps({'"'name:[lon,lat,"",[] for name,lon,lat in dict_list.items()}, indent=4)
#print json.dumps(dict_list)
outstring = "{"
for item in dict_list:
	outstring += str("\"{}\":[{},{},\"\",[]],".format(item.get("name"),item.get("lon"),item.get("lat")))
outstring+="}"
with open(route+'.json', 'w') as f:
	f.write(outstring)
print outstring
