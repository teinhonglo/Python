import collections
import operator
from pprint import pprint  # pretty-printer

def dict2List(dct):
	lst = []
	if type(dct1.values()[0]) == type({}):
		for d in dct1.values():
			lst.append(dict2List(d))
	else:	
		dct1 = collections.OrderedDict(dct)
		return dct.values()
	return lst	

dct = {	3:
			{2:
				{2:3, 1:89, 4:5, 3:0}, 
			1:
				{2:3, 1:89, 4:5, 3:0}, 
			4:
				{2:3, 1:89, 4:5, 3:0}, 
			3:
				{2:3, 1:89, 4:5, 3:0}
			}, 
		4:
			{2:
				{2:3, 1:89, 4:5, 3:0}, 
			1:
				{2:3, 1:89, 4:5, 3:0}, 
			4:
				{2:3, 1:89, 4:5, 3:0}, 
			3:
				{2:3, 1:89, 4:5, 3:0}
			},
		1:
			{2:
				{2:3, 1:89, 4:5, 3:0}, 
			1:
				{2:3, 1:89, 4:5, 3:0}, 
			4:
				{2:3, 1:89, 4:5, 3:0}, 
			3:
				{2:3, 1:50, 4:5, 3:0}
			}, 
		2: {"a":
				{2:6, "c":11, 4:98, 3:10}, 
			"b":
				{2:3, 1:89, 4:5, 3:0}, 
			"c":
				{2:3, 1:89, 4:5, 3:0}, 
			"d":
				{2:3, 1:89, 4:5, 3:0}
			}
		}
pprint(dict2List(dct))
