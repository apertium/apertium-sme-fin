#!/usr/bin/env python2.6
import os, sys, getopt
import subprocess as sp
P = sp.PIPE

GTHOME = "/Users/pyry/gtsvn"
OMORFI = "%s/kt/fin/omorfi" % GTHOME
FINCG = "%s/kt/fin/src/fin-dis.bin" % GTHOME

# TODO: automake in apertium and gtsvn when files differ?

steps = [a.split(' ') for a in 
	[
		"hfst-proc %s/src/mor-omorfi.apertium.hfst" % OMORFI,
		"cg-proc -w %s" % FINCG,
		"apertium-tagger -g fin-sme.prob",
		"apertium-transfer apertium-sme-fin.fin-sme.t1x fin-sme.t1x.bin fin-sme.autobil.bin",
		# "apertium -d . fin-sme-chunker",
		"hfst-proc -g fin-sme.autogen.hfst",
	]
]

def split_output(text=sys.stdin.read()):
	
	outputs = []
	input = text.replace('\n','')
	
	kwargs = {'shell': False, 'stdout': P, 'stdin':P}
	for step in steps:
		output = sp.Popen(step, **kwargs).communicate(input + '\n')
		input = output[0].replace('\n','')
		outputs.append(input)
			
	print '\n'.join(outputs)

split_output()
