#!/usr/bin/env python
# encoding: utf-8
"""
apertium.py

Created by pyry on 2010-07-01.
"""

import os, sys, getopt
import subprocess as sp
import re
import hashlib
import pickle

# TODO: change this
APERTIUM_DIR = '/Users/pyry/apertium/apertium-sme-fin/'

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


# TODO: Cache all inputs and outputs

def apertium(data, subcommand=None, cache=True, debug=False, opts=" "):
	kwargs = {'shell': False, 'stdout': PIPE, 'stdin':PIPE}

	if subcommand:
		cmd = 'apertium %s -d %s fin-sme-%s' % ((opts, APERTIUM_DIR, subcommand)) 
	else:
		cmd = 'apertium %s -d %s fin-sme' % (opts, APERTIUM_DIR)

	# Coercing data	
	if type(data) == list:
		data = ''.join(data)

	if type(data) == unicode:
		try:
			data = data.encode('utf-8')
		except Exception, e:
			raise e

	if cache:
		cache_exists = cache_data(cmd, data, debug)

		if type(cache_exists) == False:
			output = Popen(cmd, data)
			if cache:
				F = open(cache_name, 'w')
				pickle.dump(output, F)
			else:
				output = cache_exists
	else:
		output = Popen(cmd, data)
	
	return output



