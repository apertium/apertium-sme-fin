#!/usr/bin/env python2.6
# encoding: utf-8

import os, sys, getopt
import subprocess as sp
P = sp.PIPE

GTHOME = "/Users/pyry/gtsvn"
FIN = GTHOME + "/kt/fin/"
OMORFI = "%s/kt/fin/omorfi/src" % GTHOME
# OMORFI = "/opt/local/share/omorfi"
FINCG = "%s/kt/fin/src/fin-dis.bin" % GTHOME

# TODO: automake in apertium and gtsvn when files differ?

steps = [a.split(' ') for a in 
	[
		"hfst-proc %s/mor-omorfi.apertium.hfst" % OMORFI,
		# "cg-proc -w %s" % FINCG,
		"preprocess | hfst-lookup /opt/local/share/omorfi/mor-omorfi.cg.hfst | /Users/pyry/apertium/apertium-sme-fin/tools/lookup2cg | vislcg3 -g /Users/pyry/apertium/apertium-sme-fin/src/fin-dis.rle",
		"./switch-label.py"
		"apertium-tagger -g fin-sme.prob",
		"apertium-transfer apertium-sme-fin.fin-sme.t1x fin-sme.t1x.bin fin-sme.autobil.bin",
		# "apertium -d . fin-sme-chunker",
		"hfst-proc -g fin-sme.autogen.hfst",
	]
]

def split_output(text=False):
	if not text:
		text = sys.stdin.read()
	
	outputs = []
	input = text.replace('\n','')
	
	kwargs = {'shell': True, 'stdout': P, 'stdin':P}
	for step in steps:
		output = sp.Popen(step, **kwargs).communicate(input + '\n')
		input = output[0].replace('\n','')
		outputs.append(input)
			
	print '\n'.join(outputs)


CWD = os.curdir
FINCG = "preprocess | hfst-lookup /opt/local/share/omorfi/mor-omorfi.cg.hfst | /Users/pyry/apertium/apertium-sme-fin/tools/lookup2cg | vislcg3 -g /Users/pyry/apertium/apertium-sme-fin/dev/gtsvn/kt/fin/src/fin-dis.rle --trace"
FINCGT = "hfst-proc -w /Users/pyry/apertium/apertium-sme-fin/fin-sme.automorf.hfst | /Users/pyry/apertium/apertium-sme-fin/dev/tagger-to-visl.py | vislcg3 --trace --grammar /Users/pyry/apertium/apertium-sme-fin/fin-sme.rlx.bin"

def watch(dir_to_watch, command):
	"""
		Watches a directory for file additions updates or saves, then runs a command; clearing screen.
	"""
	import os, time
	os.system("clear")
	os.system(command)
	path_to_watch = dir_to_watch
	before = dict ([(f, [None, os.stat(f).st_mtime]) for f in os.listdir (path_to_watch)])
	
	while 1:
		time.sleep(1)
		after = dict ([(f, [None, os.stat(f).st_mtime]) for f in os.listdir (path_to_watch)])
		added = [f for f in after if not f in before]
		removed = [f for f in before if not f in after]
		
		if added or removed:
			updated = None
		else:
			updated = [f for f, k in after.items() if before[f][1] != after[f][1]]
		
		if added: print "Added: ", ", ".join (added)
		if removed: print "Removed: ", ", ".join (removed)
		if updated: print "Updated: ", ", ".join(updated)
		
		if added or updated or removed:
			os.system("clear")
			os.system(command)
		before = after

import getopt


help_message = '''
-c/--clean	Make clean in apertium-sme-fin and GTHOME/kt/fin/src
-r/--remake	Make all in apertium-sme-fin and GTHOME/kt/fin/src
-i/--in		Read from stdin after --clean and --remake
-e/--exec	Run this command when --watch'ing
-w/--watch	Watch a directory
With no options, this script expects piped input. Otherwise, options are processed first.'''


class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "hrciew:v", ["help", "remake", "clean", "in", "exec=", "watch="])
		except getopt.error, msg:
			raise Usage(msg)

		# option processing
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-h", "--help"):
				print help_message
			if option in ("-c", "--clean"):
				p = sp.Popen(["make", "clean"])
				p.wait()
				os.system("cd %ssrc/ && make -f Makefile clean" % FIN)
			if option in ("-r", "--remake"):
				p = sp.Popen(["make"])
				p.wait()
				os.system("cd %ssrc/ && make -f Makefile" % FIN)
			if option in ("-i", "--in"):
				split_output()
			if option in ("-e", "--exec"):
				command = value
				if command.startswith("\"") and command.endswith("\""):
					command = command[1:len(command)-1]
				if command == "fincgt":
					command = FINCGT
					imput = sys.stdin.read()
					command = "echo \"%s\" | %s" % ((imput, command))
				if command == "fincg":
					command = FINCG
					imput = sys.stdin.read()
					command = "echo \"%s\" | %s" % ((imput, command))
			if option in ("-w", "--watch"):
				dir_to_watch=value
				watch(dir_to_watch, command)
		
		if len(opts) == 0:
			split_output()

	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2


if __name__ == "__main__":
	sys.exit(main())


# split_output()
