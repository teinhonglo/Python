# Note - this code must run in Python 2.x and you must download
# http://www.pythonlearn.com/code/BeautifulSoup.py
# Into the same folder as this program

import urllib
import re
from BeautifulSoup import *

while True:
    url = raw_input('Enter - ')
    result = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', url)
    print result
    if len(result) > 0:
        break


html = urllib.urlopen(url).read()
soup = BeautifulSoup(html)

# Retrieve all of the anchor tags
tags = soup('span')
count = len(tags)
totalNum = 0

for tag in tags:
    # Look at the parts of a tag
    totalNum += int(tag.contents[0])

print "Count", count
print "Sum", totalNum
