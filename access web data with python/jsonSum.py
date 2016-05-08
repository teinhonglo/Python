import urllib
import json

url = raw_input("Enter location:")
print "Retrieving location:", url
uh = urllib.urlopen(url)
data = uh.read()
info = json.loads(data)
print 'Retrieved', len(data), 'characters'
#print json.dumps(info, indent = 4)
totalSum = 0

for comment in info['comments']:
    totalSum += int(comment['count'])
    #print comment['name']
print len(info['comments'])
print totalSum
