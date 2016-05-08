import urllib
import xml.etree.ElementTree as ET

while True:
    url = raw_input('Enter location: ')
    if url == '0':		break
    print 'Retrieving', url
    uh = urllib.urlopen(url)
    data = uh.read()
    print 'Retrieved',len(data),'characters'
    tree = ET.fromstring(data)

    counts = tree.findall('.//count')
    countLength = len(counts)
    total = 0

    for count in counts:
        total += int(count.text)

    print "Count", countLength
    print "Sum", total
