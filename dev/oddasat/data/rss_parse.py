#!/usr/bin/env python
# encoding: utf-8
"""
rss_parse.py
"""

import sys
import os
import re

from urllib2 import urlopen 
from contextlib import closing as close


from xml.dom.minidom import parse, parseString
from datetime import datetime

try:
	from feedparser import _getCharacterEncoding as enc
except ImportError:
	# sys.stderr.write('rss_parse.py: no feedparser\n')
	enc = lambda x, y: ('utf-8', 1)

# tag_regex = re.compile(r'<(?P<tag>[\w\d]+)>(\<\!\[CDATA\[)?(?P<inner>.*)(\]\]\>)?<\/[\w\d]+>')
tag_regex = re.compile(r'<(?P<tag>[\w\d]+)>(?P<inner>.*)<\/[\w\d]+>')

def node1(node, item):
	return node.getElementsByTagName(item)[0]


def getData(node):
	return tag_regex.match(node.toxml()).group('inner')

def join_or_node1(node, item):
	return ', '.join([getData(a) for a in node.getElementsByTagName(item)])

# Thu, 01 Jul 2010 02:09:23 +0300
# Wed, 7 Jul 2010 18:24:42 +0300
dmatch = re.compile(r'^(?P<day>\w{3}), (?P<date>\d{1,2}) (?P<month>\w{3}) (?P<year>\d{4}) (?P<hh>\d{2}):(?P<mm>\d{2}):(?P<ss>\d{2}) (?P<utm_a>\W)(?P<utm_b>\d{4})$')

monthint = {
	'Jan': 1,
	'Feb': 2,
	'Mar': 3,
	'Apr': 4,
	'May': 5,
	'Jun': 6,
	'Jul': 7,
	'Aug': 8,
	'Sep': 9,
	'Oct': 10,
	'Nov': 11,
	'Dec': 12
}

def fixDate(d_str):
	# Thu, 01 Jul 2010 01:20:10 +0300
	date = dmatch.match(d_str).groups()
	# ('Thu', '01', 'Jul', '2010', '01', '20', '10', '+', '0300')
	args = [int(a) for a in [date[3], monthint[date[2]], date[1], date[4], date[5]]]
	return datetime(*args)

class Article_Old(object):
	def __init__(self, n):
		Exceptions = (AttributeError, IndexError)
		
		try:						self.title = getData(node1(n, 'title')).replace(']]>', '').replace('<![CDATA[', '')
		except Exceptions:			self.title = None
		
		try:						self.url = getData(node1(n, 'link'))
		except Exceptions:			self.url = None
		
		try:						self.date = fixDate(getData(node1(n, 'pubDate')))
		except Exceptions:			self.date = None
		
		try:						self.description = getData(node1(n, 'description'))
		except Exceptions:			self.description = None
		
		try:						self.category = join_or_node1(n, 'category')
		except Exceptions: 			self.category = None
		
		if not self.title and self.url and self.date and self.description:
			self.empty = True
		else:
			self.empty = False
		
		
		return None
	def __str__(self):
		return "<Article: %s>" % str(self.title.encode('utf-8'))
		
		
	__unicode__ = __repr__ = __str__

class Article(object):
	def __init__(self, n):
		for k, v in n.iteritems():
			self.__setattr__(k, v)
		self.pub_date = fixDate(self.updated)
		


def parseRSS_old(data, intype='file'):
	"""
		Expects filename or data
	"""
		
	if intype == 'file':
		doc = parse(data)
	elif intype == 'string':
		try:
			data = data.encode('utf-8')
		except:
			pass
		doc = parseString(data)
		
	items = doc.getElementsByTagName('item')
	articles = []
	for a in items:
		new_article = Article(a)
		if not new_article.empty:
			articles.append(new_article)
		
	
	return articles

import feedparser

def parseRSS(url='http://www.iltalehti.fi/rss/rss.xml'):
	fp = feedparser.parse(url)
	
	articles = [Article(dict(item)) for item in fp['items']]
	# for item in fp['items']:
	# 	print type(dict(item))
	# 	
	# 	a = Article(dict(item))
	# 	print a.title
	return articles

def getURL(url):
	try:
		with close(urlopen(url)) as j:
			text = j.read()
			encoding = enc(j.headers, text)[0]
			if encoding == 'us-ascii':
				encoding = 'utf-8'
			data = text.decode(encoding)
	except Exception, e:
		data = text.decode('latin-1')
	except Exception, e:
		print Exception, e
		print encoding
	
	
	if data == None:
		raise e
	return data


def loadFile(fname='uutiset.rss'):
	"""
		>>> data = loadFile('uutiset.rss')
		>>> data2 = loadFile('hs.rss')
	"""
	with open(fname) as F:
		data = F.read()
	
	return data


def fetchURL(url='default'):
	"""
		Fetches URL. Doesn't actually fetch for now, just test data. Too lazy to futz with urllib
		
		>>> data = fetchURL('http://www.hs.fi/uutiset/rss/')
		>>> data = fetchURL('feed://yle.fi/uutiset/rss/uutiset.rss')
		>>> data = fetchURL('http://www.iltalehti.fi/rss/rss.xml')
		
	"""
	if url == 'default':
		with open('/Users/pyry/apertium/oddasat/data/uutiset.rss') as f:
			text = f.read()
	elif url == 'article':
		with open('/Users/pyry/apertium/oddasat/data/article.tmp') as f:
			text = f.read()
	else:
		if url.startswith('feed://'):
			url = url.replace('feed://', 'http://')
		text = getURL(url)
	return text # articles



def dummytest():
	"""		
		>>> data = loadFile('uutiset.rss')
		>>> articles = parseRSS(data, intype='string')
		
		>>> data = loadFile('hs.rss')
		>>> articles = parseRSS(data, intype='string')
		
		>>> data = loadFile('iltalehdet.xml')
		>>> articles = parseRSS(data, intype='string')
		
	"""
	
	# data = loadFile('iltalehdet.xml')
	# articles = parseRSS(data, intype='string')
	# print articles
	
	# data = loadFile('uutiset.rss')
	# articles = parseRSS(data, intype='string')
	# print articles
	# # print len(articles)
	# data = fetchURL('http://www.iltalehti.fi/rss/rss.xml')
	return True


# a = parseRSS()
# for aa in a:
# 	print aa.pub_date