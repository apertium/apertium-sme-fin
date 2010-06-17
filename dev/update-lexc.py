#!/usr/bin/python2.6

import os, sys, getopt
import subprocess as sp
import re

PIPE = sp.PIPE

class Config(object):
	def __init__(self):
		self.set_defaults()
		
	def set_defaults(self):
		"""
			Set default options. Don't change them here if you're editing the file. Change below.
		"""
		self.TARGET_LANGUAGE = "sme"
		self.SOURCE_LANGUAGE = "fin"
		self.GTHOME = os.environ.get("GTHOME")
		self.PRODUCE_LEXC_FOR = "sme"
		self.OUTPUT_DIR = '.'
		self.GTPFX = 'gt'
		
		self.SRC = '/omg/'
		
		proc_lang = self.PRODUCE_LEXC_FOR

		self.HEADER = "sme-lex.txt"
		
		# List of lists, first item is filename, second item is action 'clip' or 'cat', third is dictionary of options.
		self.files = [
			["verb-sme-lex.txt", 	'clip', 	{'pos_filter': 'V', 'split': 'VerbRoot\n'}],
			["punct-sme-lex.txt", 			'cat']
		]
		
		return True
	
	def return_dict(self):
		D = {
			"TARGET_LANGUAGE": self.TARGET_LANGUAGE,
			"SOURCE_LANGUAGE": self.SOURCE_LANGUAGE,
			"GTHOME": self.GTHOME,
			"GTPFX": self.GTPFX,
			"OUTPUT_DIR": self.OUTPUT_DIR,
			"PRODUCE_LEXC_FOR": self.PRODUCE_LEXC_FOR,
			"files": self.files
		}
		return D
	
	def read_from_dict(self, D):
		# convert all arguments to str, json module is a little funny
		for k, v in D.items():
			if type(k) == unicode:
				a = str(k)
			if type(v) == unicode:
				b = str(v)
			self.__setattr__(a, b)
			if a == 'files':
				print a
				print b
		
		self.files = D['files']
		self.SRC = SRC = self.GTHOME + '/' + self.GTPFX + '/' + self.PRODUCE_LEXC_FOR + '/src/'

class Configs(object):
	def __init__(self):
		self.langs = [Config()]

#########
# 
#  Set these options here for default behavior, or use commandline to pass in arguments. See --help.
#
#########

CONF = Configs()

CONF.langs[0].TARGET_LANGUAGE = "sme"
CONF.langs[0].SOURCE_LANGUAGE = "fin"
CONF.langs[0].GTHOME = os.environ.get("GTHOME")
CONF.langs[0].PRODUCE_LEXC_FOR = "sme"
CONF.langs[0].OUTPUT_DIR = os.getcwd() + '/../'
CONF.langs[0].GTPFX = 'gt'
CONF.langs[0].HEADER = "sme-lex.txt"
CONF.langs[0].SRC = CONF.langs[0].GTHOME + '/' + CONF.langs[0].GTPFX + '/' + CONF.langs[0].PRODUCE_LEXC_FOR + '/src/'

CONF.langs[0].files = [
	["verb-sme-lex.txt", 	'clip', 	{'pos_filter': 'V', 'split': 'VerbRoot\n'}],
	["noun-sme-lex.txt", 	'clip', 	{'pos_filter': 'N', 'split': 'NounRoot\n'}],
	["adj-sme-lex.txt", 		'clip', 	{'pos_filter': 'A', 'split': 'AdjectiveRoot\n'}],
	["propernoun-sme-morph.txt", 	'cat'],
	["propernoun-sme-lex.txt", 'clip', 	{'pos_filter': 'N><Prop', 'split': 'ProperNoun\n'}],
	["conjunction-sme-lex.txt", 	'cat'],
	["adv-sme-lex.txt", 		'clip', 	{'pos_filter': 'Adv', 'split': 'Adverb'}],
	["adv-sme-lex.txt", 		'clip', 	{'pos_filter': 'Adv', 'split': 'gadv ! adv that can form compounds', 'no_header': True, 'no_trim': True}],
	["subjunction-sme-lex.txt", 	'cat'],
	["pronoun-sme-lex.txt", 		'cat'],
	["particle-sme-lex.txt", 		'cat'],
	["pp-sme-lex.txt", 			'cat'],
	["numeral-sme-lex.txt", 		'cat'],
	["abbr-sme-lex.txt", 			'cat'],
	["punct-sme-lex.txt", 			'cat']
]

try:
	import json
except ImportError:
	print "json module not installed. Only command line options or options in this file will be possible."

if json:
	try:
		with open('langs.cfg', 'r') as F:
			exists = True
			try:
				D = json.load(F)
			except Exception, e:
				print e
			CONF = Configs()
			if len(D) == 1:
				new = Config()
				new.read_from_dict(D[0])
				CONF.langs = [new]
			elif len(D) > 1:
				CONF.langs = []
				for item in D:
					new = Config()
					new.read_from_dict(item)
					CONF.langs.append(new)
			print CONF.langs		
			print "Loaded config from %s" % F.name
			
	except IOError:
		print "Config file does not exist. Creating default file."
		with open('langs.cfg', 'w') as F:
			json.dump([CONF.langs[0].return_dict()], F, ensure_ascii=True)
			print "Defaults saved to %s" % F.name
else:
	json == False


# 	Regexp to exclude lines we don't want
lex_excludes = [
	'\!\^NG\^',
	'; \!SUB',
	'\! \!SOUTH',
	'\+Use\/NG',
	'\+Nom(.*)\+Use\/Sub',
	'\+Gen(.*)\+Use\/Sub',
	'\+Use\/Sub(.*)\+V\+TV',
	'\+Attr(.*)\+Use\/Sub',
	'LEXICON PRSPRCTOADJ \!SUB',
	'\+Imprt(.*)\+Use\/Sub'	
]
excl = re.compile(r'|'.join(['(?:' + a + ')' for a in lex_excludes]))


def lt_exp(fname, side=None):
	"""
		Expands lexicon file, currently only one-sided.
		
		TODO: Two sides!
	"""
	
	cmd = "lt-expand %s" % fname
	ltexp = sp.Popen(cmd.split(' '), shell=False, stdout=PIPE, stderr=PIPE, stdin=PIPE)
	output = ltexp.communicate()[0].splitlines() # split('\n')
	
	# Remove REGEX and empty lines
	output = [l for l in output if "REGEX" not in l and l.strip()]
	
	return output


def cat_file(fname, ret_type=False, exclude=False):
	"""
		Get data from file, if exclude=True, then exclude lines; otherwise return all data.
		
		Returns list.
	"""
	
	with open(fname, 'r') as F:
		lines = F.readlines()
		if exclude:
			data = [a for a in lines if not excl.search(a)]
		else:
			data = lines
	
	if ret_type:
		if ret_type == list:
			return data
		elif ret_type == str:
			return ''.join(data)
	else:
		return data


def extract(data, fname, pos_filter, split, no_header=False, no_trim=False, debug=False):
	"""
		Given a pattern (e.g., V, N, N><Prop), extract matching intersecting words between lt-expanded data and lex file (fname).
		
		data (list) 		- lt-expanded data.
		fname (str) 		- File name to read.
		split (str) 		- Split after this point in a file, f. ex.: 'NounRoot\\n' splits at 'LEXICON NounRoot\n'
		pos_filter (str) 	- Filter lines based on pattern, e.g., V, N, N><Prop, etc. Will be turned to <V, <N, etc.
		no_header (bool) 	- False by default, if true, do not return header.
		no_trim (bool) 		- False by default, if true, do not filter based on pos_filter
		
	"""
		
	if pos_filter:
		search_key = '<' + pos_filter
	else:
		search_key = False
		
	# Words matching pos
	
	rx_spl = re.compile(r'\<').split
	l_split = lambda x: rx_spl(x)[0]	
	
	# Possible to do this faster?	
	if search_key:
		words = list(set([l_split(a) for a in data if a.find(search_key) > -1]))
	else:
		words = list(set([l_split(a) for a in data]))
	
	if debug:
		print str(len(words)) + ' unique words matching %s in .dix' % (str(search_key), fname.lower())
	
	# May not be excluding commented lines, probably should.
	with open(fname, 'r') as F:
		text = F.read()
	point = 'LEXICON %s' % split
	
	# split text
	clip = text.split(point)
	head = clip[0] + '\n' + point + '\n'
	try:
		rest = clip[1] # NOTE: point not added back in
	except IndexError:
		rest = text
	
	if debug:
		print rest
	
	# Filter out text based on excludes
	rest = rest.splitlines()
	rest = [a for a in rest if not excl.search(a)]
		
	# rest = [a for a in rest if not a.startswith('!')]
	
	# if this is slow, there is still something creative that can be done here
	
	# regex isn't working for some reason.
	chstr = re.compile(r'[0\^\#]').sub
	chspl = re.compile(r'(:|\+)').split
	
	stripchar = lambda x: chstr('', chspl(x)[0])
	
	# Slow
	# stripchar = lambda x: x.replace('0','').replace('^','').replace('#','').partition(':')[0].partition('+')[0]
	
	if no_trim:
		trim = rest
	else:
		# trim = map(stripchar, )
		trim = [a for a in rest if stripchar(a.strip()) in words]
	
	trim = '\n'.join(trim)
	
	if no_header:
		return '\n', "%s\n%s" % (point, trim)
	else:
		return head, trim


def make_lexc(TL, SL, proc_lang, gthome, gtpfx, out_dir, COBJ=False):
	"""
		This does everything.
		
		TODO: SRC dir should be moved out of here, passed in instead for easier switching of languages? /gt/ ~ /kt/ stuff will confuse things.
		TODO: error handling if files don't exist.
		
		COBJ = Config object
	"""
	
	# Prefix direction
	PREFIX1 = "%s-%s" % (TL, SL)
	PREFIX2 = "%s-%s" % (SL, TL)
	
	# Project base-name
	BASENAME = "apertium-" + PREFIX1
	
	# if not GTHOME:
	# 		print "$GTHOME not set."
	# 		sys.exit() # TODO: exit with error
	
	# SRC = "%s/%s/%s/src" % (gthome, gtpfx, proc_lang)
	SRC = COBJ.SRC
	
	DEV = os.getcwd()
	OUTFILE = "%s.%s.lexc" % (BASENAME, proc_lang) # TODO: change to prod location.
	
	# Get data from lt_expand
	lt_expand_data = lt_exp(fname="%s/../%s.%s.dix" % (DEV, BASENAME, PREFIX1))
	main_header = cat_file(COBJ.SRC + "/" + COBJ.HEADER, list, exclude=True)
	
	# Use dicts to go through files and trim
	# strings for just reading a filename with no action taken
	
	# Add SRC dir to STEPS
	STEPS = COBJ.files
	
	output_ = [''.join(main_header)]
	output_app = output_.append			# Faster this way
	
	for step in STEPS:
		fname, action = SRC + step[0], step[1]
		
		if len(step) == 3:		opts = dict([(str(a), str(b)) for a, b in step[2].items()])
		else:					opts = None
				
		try:
			with open(fname, 'r') as F:
				exists = True			
		except IOError, e:
			print "*** File %s does not exist. Skipping. ***" % fname
			continue
	
		if action == 'clip':
			print "... Fetching words from %s" % fname
			if opts:
				head, trim = extract(lt_expand_data, fname, **opts)
			else:
				head, trim = extract(lt_expand_data, fname)
			data = head + trim
		elif action == 'cat':
			print "... Reading all of %s" % fname
			data = cat_file(fname, str, exclude=False)
		
		output_app(data)
		
	# TODO:
	# punct_point=`grep -nH ' real pilcrow' $PUNCTLEXC | cut -f2 -d':'`;
	# head -n $punct_point $PUNCTLEXC >> $OUTFILE;
	
	out_ = '\n'.join([a for a in output_])
	OUTFILE = out_dir + OUTFILE
	
	with open(OUTFILE, 'w') as F:
		F.write(out_)
	
	print '... Done.'
	print 'Saved to %s.\n' % OUTFILE
	return True


### Begin command-line and input handling

default_values = '\n'
default_values += "\t--target-lang:   %s\n" % CONF.langs[0].TARGET_LANGUAGE
default_values += "\t--source-lang:   %s\n" % CONF.langs[0].SOURCE_LANGUAGE
default_values += "\t--proc-lang:     %s\n" % CONF.langs[0].PRODUCE_LEXC_FOR
default_values += "\t--gthome:        %s\n" % CONF.langs[0].GTHOME
default_values += "\t--gt-prefix:     %s\n" % CONF.langs[0].GTPFX
default_values += "\t--output-dir:    %s\n" % CONF.langs[0].OUTPUT_DIR
default_values += "\n\tDefault proc dir: %s\n" % "%s%s/%s/src/" % (CONF.langs[0].GTHOME, CONF.langs[0].GTPFX, CONF.langs[0].PRODUCE_LEXC_FOR)


help_message = '''\n\nOPTIONS:
	-t/--target-lang	
	-s/--source-lang	
	-p/--proc-lang	Language to process lexc files for
	-g/--gthome	Giellatekno source repository
	-x/--gt-prefix	Giellatekno subdirectory, e.g., gt, kt.
	-o/--output-dir	Location to output to. Default is one up from /dev/
	
DEFAULT VALUES IN FILE:
'''

help_message += default_values

help_message += """
Currently which -lex.txt files are processed is specified in a somewhat complicated way, however
if one file is missing, then the file skips and processing should continue anyway.  It is likely
that something else  will be needed for this,  since the .lexc files programmed in  are specific
to sme. 
"""

class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg

# make_lexc(TL=TARGET_LANGUAGE, SL=SOURCE_LANGUAGE, proc_lang=PRODUCE_LEXC_FOR, gthome=GTHOME, gtpfx=GTPFX, out_dir=OUTPUT_DIR):

def main(argv=None):
	
	# Set commandline defaults
	cmd_tl            = CONF.langs[0].TARGET_LANGUAGE
	cmd_sl            = CONF.langs[0].SOURCE_LANGUAGE
	cmd_proc_lang     = CONF.langs[0].PRODUCE_LEXC_FOR
	cmd_gthome        = CONF.langs[0].GTHOME
	cmd_gtpfx         = CONF.langs[0].GTPFX
	cmd_outdir        = CONF.langs[0].OUTPUT_DIR
	
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "tspgxho:v", ["help", "target-lang=", "source-lang=", "proc-lang=", "gthome=", "gt-prefix=", "output-dir="])
		except getopt.error, msg:
			raise Usage(msg)

		# option processing
		if len(opts) == 0:
			print "\nNo options, using defaults in file, or langs.cfg."
			print "See --help for more information. \n"
			for lang in CONF.langs:
				make_lexc(
					lang.TARGET_LANGUAGE, 
					lang.SOURCE_LANGUAGE, 
					lang.PRODUCE_LEXC_FOR,
					lang.GTPFX,
					lang.GTHOME,
					lang.OUTPUT_DIR,
					lang
				)
		
			# if len(CONF.langs) == 1:
			# 	lang = CONF.langs[0]
			# 	make_lexc(
			# 		lang.TARGET_LANGUAGE, 
			# 		lang.SOURCE_LANGUAGE, 
			# 		lang.PRODUCE_LEXC_FOR,
			# 		lang.GTPFX,
			# 		lang.GTHOME,
			# 		lang.OUTPUT_DIR,
			# 		lang
			# 	)
			# elif len(CONF.langs) > 1:
			# 	for lang in CONF.langs:
			# 		make_lexc(
			# 			lang.TARGET_LANGUAGE, 
			# 			lang.SOURCE_LANGUAGE, 
			# 			lang.PRODUCE_LEXC_FOR,
			# 			lang.GTPFX,
			# 			lang.GTHOME,
			# 			lang.OUTPUT_DIR,
			# 			lang
			# 		)
			
							
		elif len(opts) > 0:			
			for option, value in opts:
				if option == "-v":
					verbose = True
				if option in ("-h", "--help"):
					raise Usage(help_message)
				if option in ("-t", "--target-lang"):
					cmd_tl = value
				if option in ("-s", "--source-lang"):
					cmd_sl = value
				if option in ("-p", "--proc-lang"):
					cmd_proc_lang = value
				if option in ("-g", "--gthome"):
					cmd_gthome = value
				if option in ("-x", "--gt-prefix"):
					cmd_gtpfx = value
				if option in ("-o", "--output-dir"):
					cmd_outdir = value
		
			make_lexc(cmd_tl, cmd_sl, cmd_proc_lang, cmd_gtpfx, cmd_gthome, cmd_outdir)


	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "For help use --help.\n"
		return 2


if __name__ == "__main__":
	# make_lexc()
	sys.exit(main())



