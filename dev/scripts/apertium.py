#!/usr/bin/env python
# encoding: utf-8
"""
apertium.py

Created by pyry on 2010-06-24.
Collection of apertium-related tools.
"""

import os, sys, getopt
import subprocess as sp
import re
import hashlib
import pickle

# TODO: change this
APERTIUM_DIR = '/Users/pyry/apertium/apertium-sme-fin/'

# TODO: check for cache directory, create if not existing

PIPE = sp.PIPE
class ApertiumError(Exception):
	def __init__(self, msg):
		print "Apertium had some errors:"
		print msg

class LTExpError(Exception):
	def __init__(self, msg):
		print "lt-expand failed processing. Error:"
		print msg

class CmdError(Exception):
	def __init__(self, cmd, msg):
		print "error running: %s" % cmd
		print msg


# TODO: general datatype coerce function

def Popen(cmd, inp=False, ret_err=False):
	proc = sp.Popen(cmd.split(' '), shell=False, stdout=PIPE, stderr=PIPE, stdin=PIPE)
	if inp:
		if type(inp) == str:
			try:
				inp = inp.encode('utf-8')
			except UnicodeDecodeError:
				pass
			except Exception, e:
				print "omg"
				print Exception, e
				omg
		if type(inp) == unicode:
			try:
				inp = str(inp)
			except Exception, e:
				print "omg"
				print e
				omg
		kwargs = {'input': inp}
	else:
		kwargs = {}
		
	output, err = proc.communicate(**kwargs)
	try:
		if err:
			raise CmdError(cmd, err)
	except CmdError:
		pass
		
	if ret_err:
		return output, err
	else:
		return output



def cache_data(cmd, data, debug=False):
	"""
		Take some data, cache it, return data. If cache exists, load from that.
	"""
	cache_name = '/tmp/py_caches/cache_' + hashlib.sha1(cmd + data).hexdigest()
	cache_exists = os.path.isfile(cache_name)
	
	if cache_exists:
		if debug:
			print "*** Using cache...\n"
		F = open(cache_name, 'r')
		try:
			output = pickle.load(F)
		except EOFError:
			print "*** Cache file (%s) empty" % cache_name	
		
		return output
	else:
		return False


# can cache the stuff in here too.
def lt_exp(fname):
	"""
		Validates for errors in dix, then returns expanded data.		
	"""
	
	output, err = Popen("apertium-validate-dictionary %s" % fname, ret_err=True)
	
	if len(err) > 0:
		raise LTExpError(err)
	
	output, err = Popen("lt-expand %s" % fname, ret_err=True)
	if len(err) > 0:
		raise LTExpError(err)
		
	# Remove REGEX and empty lines
	output = [l for l in output.splitlines() if "REGEX" not in l and l.strip()]
	
	return output


# TODO: Cache all inputs and outputs
def apertium(data, subcommand=None, cache=True, debug=False):
	kwargs = {'shell': False, 'stdout': PIPE, 'stdin':PIPE}
	
	if subcommand:
		cmd = 'apertium -d %s fin-sme-%s' % ((APERTIUM_DIR, subcommand)) 
	else:
		cmd = 'apertium -d %s fin-sme' % APERTIUM_DIR
	
	# Coercing data	
	if type(data) == list:
		data = ''.join(data)
	
	if type(data) == unicode:
		try:
			data = data.encode('utf-8')
		except Exception, e:
			raise e
	
	cache_exists = cache_data(cmd, data, debug)
		
	if type(cache_exists) == False:
		output = Popen(cmd, data)
		if cache:
			F = open(cache_name, 'w')
			pickle.dump(output, F)
	else:
		output = cache_exists
	
	return output


def test():
	# TODO: test with no debug to see if all messages are supressed
	d = True
	
	fin_sentence = u'Minä näin kaksi koiraa.'
	print "Testing Apertium: %s" % fin_sentence
	print apertium(fin_sentence, debug=True)
	print "Testing Apertium chunker: %s" % fin_sentence
	print apertium(fin_sentence, subcommand='chunker', debug=d)
	print "Testing Apertium tagger: %s" % fin_sentence
	print apertium(fin_sentence, subcommand='tagger', debug=d)
	# bidix = '/Users/pyry/apertium/apertium-sme-fin/apertium-sme-fin.sme-fin.dix'
	# out_ = lt_exp(bidix)
	# print ''.join(out_)

def main():
	# test()
	pass


if __name__ == '__main__':
	main()

