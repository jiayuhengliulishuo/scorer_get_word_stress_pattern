#!/usr/bin/python

import re
import sys
import pickle
import csv
from os.path import basename
dict_file='cmu07_20140625.sdic'
dictionary = {}
for line in open(dict_file).readlines():
	m = re.match(r'^(\S+)\s+(.*)$', line.strip())
	dictionary[m.group(1)] = m.group(2)
outf=open('SmallDice.sdic','w')
filename='filename_trans.csv'
count1=0
count2=0
Dic={}
with open(filename) as f:
	reader=csv.reader(f)
	for row in reader:
		tokens = re.split(r'\s+', row[1].strip())		
		for word in tokens:
			
			if word in dictionary:
				if not Dic.has_key(word):
					outf.write('%s %s\n' % (word, dictionary[word]))
					count1+=1
					Dic[word]=""
			else:
				sys.stderr.write('Word %s not found\n' % word)
				count2+=1
				print word

outf.close()
print count1
print count2
