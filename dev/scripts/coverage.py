#!/opt/local/IncPy/python.exe
# encoding: utf-8

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


if __name__ == "__main__":
	sys.exit(main())