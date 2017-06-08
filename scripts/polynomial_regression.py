# -*- coding: utf-8 -*-

import csv 
import sys
import numpy as np


print "Use as follows: polynomial_regression.py <datafile> <degree>"
try:
	with open(sys.argv[1], 'rb') as f:
		reader = csv.DictReader(f)
		x = []
		y = []
		for row in reader:
	#		print row
			try:
				x.append(float(row['reality']))
				y.append(float(row['measurement']))
			except ValueError:
				print( "Could not convert '{}' to a float...skipping.".format(entry))
		coeffs = np.polyfit(x,y,sys.argv[2])
		print "The coeffs are ", coeffs
	#	p = np.poly1d(coeffs)
	#	for i in x:
	#		print p(i)
except:
	print "Something went wrong. Check for correct file format."
