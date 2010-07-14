#!/opt/local/IncPy/python.exe
# encoding: utf-8

from apertium import apertium

import sys
import getopt
import re
import string

help_message = '''
Get coverage statistics for piped in data
'''

splitter = re.compile(r'\s|\n')

excludes = '",`.;:' # don't want to exclude all punctuation
table = string.maketrans("", "")

strip_chars = lambda x: x.translate(table, excludes)

def split_words(chunk):
	if type(chunk) == list:
		data = '\n'.join(chunk)
	else:
		data = chunk
	
	data = [strip_chars(a.strip()) for a in splitter.split(data) if a.strip()]
	return data
	

fail_rexp = re.compile(r'^(?P<star>\*)|^(?P<hash>\#)|^(?P<at>\@)')
fails = lambda x: fail_rexp.findall(x) and fail_rexp.findall(x) or None

clean_fails = lambda x: tuple([1 for a in x if len(a) > 0])

def coverage(text):
	words = split_words(text)
	word_count = len(words)
	# This gives a list with tuples of ('*', '#', '@')
	matched = [a for a in [fails(word) for word in words] if a]
	star = 0
	hash_ = 0
	at = 0
	
	# Cooler way to do this? :o
	for item in matched:
		q = item[0]
		if q[0]:
			star += 1
		if q[1]:
			hash_ += 1
		if q[2]:
			at += 1
	
	# ('*', '#', '@')
	counts = ('Starred', 'Nongenerated', 'Unknown')
	
	print 'Total words: %d' % word_count
	totals =  dict(zip(counts, (star, hash_, at)))
	for k,v in totals.iteritems():
		print '\t%s: %d' % (k, v)


def main():
	text = sys.stdin.read()
	coverage(text)


if __name__ == "__main__":
	sys.exit(main())