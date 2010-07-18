#!/usr/bin/env python2.6
# encoding: utf-8

# #!/opt/local/IncPy/python.exe

import sys
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

def coverage(text):
	words = split_words(text)
	word_count = len(words)
	unique_word_count = len(list(set(words)))
	
	# This gives a list with tuples for each word with ('*', '#', '@')
	matched = [a for a in [fails(word) for word in words] if a]
	
	star, hash_, at = 0, 0, 0
	
	# Cooler way to do this? :o
	for item in matched:
		q = item[0]
		if q[0]:
			star += 1
		if q[1]:
			hash_ += 1
		if q[2]:
			at += 1
	
	tags = ('*', '#', '@')
	counts = (star, hash_, at)
	
	print >> sys.stdout, 'Total words:  %d' % word_count
	print >> sys.stdout, 'Total unique word forms:  %d\n' % unique_word_count
	totals =  dict(zip(tags, counts))
	
	div = lambda x,y: round(float(x)/float(y), 2)
	perc = lambda x: str(x*100) + '%'
	div_perc = lambda x,y: str(round(float(x)/float(y), 2)*100) + '%'
	
	
	for k,v in totals.iteritems():
		percent = div_perc(v,word_count)
		print >> sys.stdout, '\t%s:  %d\t\t%s' % (k, v, percent)
	
	print >> sys.stdout, '\nnaive total: \t\t%s' % str(perc(sum([div(a,word_count) for a in totals.values()])))
	print >> sys.stdout, 'without error: %s\t%s' % (str(word_count-sum(counts)), div_perc(word_count-sum(counts),word_count))

	print ''
	return 2 


def main():
	text = sys.stdin.read()
	coverage(text)

fails = lambda x: fail_rexp.findall(x) or None
to_count = lambda y: tuple([z and 1 or 0 for z in y])
count_ = lambda list_, index_: len([1 for b in list_ if b[index_]])

from operator import itemgetter


split_words = lambda chunk: [strip_chars(a.strip()) for a in splitter.split(chunk) if a.strip()]

def funcmain():
	words = []
	w_extend = words.extend
	word_count = 0
	
	tags = ('*', '#', '@')
	star, hash_, at = 0, 0, 0
	
	for line in sys.stdin:
		line_words = split_words(line)
		line_word_count = len(line_words)
		line_unique_word_count = len(list(set(line_words)))
		
		matched = [to_count(fails(word)[0]) for word in line_words if fails(word)]
		
		star += count_(matched, 0)
		hash_ += count_(matched, 1)
		at += count_(matched, 2)
		
		w_extend(line_words)
		word_count += line_word_count
	
	unique_word_count = len(list(set(words)))
	
	
	counts = (star, hash_, at)
	print >> sys.stdout, 'Total words:  %d' % word_count
	print >> sys.stdout, 'Total unique word forms:  %d\n' % unique_word_count
	totals =  dict(zip(tags, counts))
	
	# Calculate and return statistics
	div = lambda x,y: round(float(x)/float(y), 2)
	perc = lambda x: str(x*100) + '%'
	div_perc = lambda x,y: str(round(float(x)/float(y), 2)*100) + '%'
	
	for k,v in totals.iteritems():
		percent = div_perc(v,word_count)
		print >> sys.stdout, '\t%s:  %d\t\t%s' % (k, v, percent)
	
	print >> sys.stdout, '\nnaive total: \t\t%s' % str(perc(sum([div(a,word_count) for a in totals.values()])))
	print >> sys.stdout, 'without error: %s\t%s' % (str(word_count-sum(counts)), div_perc(word_count-sum(counts),word_count))


def itermain():
	words = []
	word_append = words.extend
	word_count = 0
	
	tags = ('*', '#', '@')
	star, hash_, at = 0, 0, 0
	
	for line in sys.stdin:
		line_words = split_words(line)
		line_word_count = len(line_words)
		line_unique_word_count = len(list(set(line_words)))
		matched = [a for a in [fails(word) for word in line_words] if a]
		
		for item in matched:
			q = item[0]
			if q[0]:
				star += 1
			if q[1]:
				hash_ += 1
			if q[2]:
				at += 1
		
		word_append(line_words)
		word_count += line_word_count
		
	unique_word_count = len(list(set(words)))
	
	counts = (star, hash_, at)
	print >> sys.stdout, 'Total words:  %d' % word_count
	print >> sys.stdout, 'Total unique word forms:  %d\n' % unique_word_count
	totals =  dict(zip(tags, counts))
	
	# Calculate and return statistics
	div = lambda x,y: round(float(x)/float(y), 2)
	perc = lambda x: str(x*100) + '%'
	div_perc = lambda x,y: str(round(float(x)/float(y), 2)*100) + '%'
	
	for k,v in totals.iteritems():
		percent = div_perc(v,word_count)
		print >> sys.stdout, '\t%s:  %d\t\t%s' % (k, v, percent)
	
	print >> sys.stdout, '\nnaive total: \t\t%s' % str(perc(sum([div(a,word_count) for a in totals.values()])))
	print >> sys.stdout, 'without error: %s\t%s' % (str(word_count-sum(counts)), div_perc(word_count-sum(counts),word_count))
	
		

# import cProfile
if __name__ == "__main__":
	# cProfile.run('funcmain()')
	sys.exit(itermain())