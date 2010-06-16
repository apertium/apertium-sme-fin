#!/usr/bin/python

import os, sys
import subprocess as sp
import re

# Some global stuff
PIPE = sp.PIPE

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


def make_lexc(TL="sme", SL="fin", proc_lang="sme", GTHOME=os.environ.get("GTHOME")):
	"""
		This does everything.
		
		TODO: SRC dir should be moved out of here, passed in instead for easier switching of languages? /gt/ ~ /kt/ stuff will confuse things.
		TODO: error handling if files don't exist.
	"""
	
	# Prefix direction
	PREFIX1 = "%s-%s" % (TL, SL)
	PREFIX2 = "%s-%s" % (SL, TL)
	
	# Project base-name
	BASENAME = "apertium-" + PREFIX1
	
	# if not GTHOME:
	# 		print "$GTHOME not set."
	# 		sys.exit() # TODO: exit with error
	
	SRC = "%s/gt/%s/src" % (GTHOME, proc_lang)
	
	DEV = os.getcwd()
	OUTFILE = "%s.%s.lexc" % (BASENAME, proc_lang) # TODO: change to prod location.
	
	# Get data from lt_expand
	lt_expand_data = lt_exp(fname="%s/../%s.%s.dix" % (DEV, BASENAME, PREFIX1))
	main_header = cat_file('%s/%s-lex.txt' % (SRC, proc_lang), list, exclude=True)
	
	# Use dicts to go through files and trim
	# strings for just reading a filename with no action taken
	
	STEPS = [
		{'fname': "%s/%s-%s-lex.txt" % (SRC, 'verb', proc_lang), 'pos_filter': 'V', 'split': 'VerbRoot\n'},
		{'fname': "%s/%s-%s-lex.txt" % (SRC, 'noun', proc_lang), 'pos_filter': 'N', 'split': 'NounRoot\n'},
		{'fname': "%s/%s-%s-lex.txt" % (SRC, 'adj', proc_lang), 'pos_filter': 'A', 'split': 'AdjectiveRoot\n'},
		"%s/propernoun-%s-morph.txt" % ((SRC, proc_lang)),
		{'fname': "%s/%s-%s-lex.txt" % (SRC, 'propernoun', proc_lang), 'pos_filter': 'N><Prop', 'split': 'ProperNoun\n'},
		"%s/conjunction-%s-lex.txt" % (SRC, proc_lang),
		{'fname': "%s/%s-%s-lex.txt" % (SRC, 'adv', proc_lang), 'pos_filter': 'Adv', 'split': 'Adverb'},
		{'fname': "%s/%s-%s-lex.txt" % (SRC, 'adv', proc_lang), 'pos_filter': 'Adv', 'split': 'gadv ! adv that can form compounds', 'no_header': True, 'no_trim': True},
		"%s/subjunction-%s-lex.txt" % (SRC, proc_lang),
		"%s/pronoun-%s-lex.txt" % (SRC, proc_lang),
		"%s/particle-%s-lex.txt" % (SRC, proc_lang),
		"%s/pp-%s-lex.txt" % (SRC, proc_lang),
		"%s/numeral-%s-lex.txt" % (SRC, proc_lang),
		"%s/abbr-%s-lex.txt" % (SRC, proc_lang),
		"%s/punct-%s-lex.txt" % (SRC, proc_lang)
	]
	
	output_ = [''.join(main_header)]
	output_app = output_.append			# Faster this way
	for step in STEPS:
		if type(step) == dict:
			try:
				with open(step['fname'], 'r') as F:
					exists = True			
				print "... Fetching words from %s" % step['fname']
				head, trim = extract(lt_expand_data, **step)
				data = head + trim
			except IOError, e:
				print "... File %s does not exist." % step['fname']
				return 2
		elif type(step) == str:
			try:
				with open(step, 'r') as F:
					exists = True
				print "... Reading all of %s" % step
				data = cat_file(step, str, exclude=False)
			except IOError, e:
				print "... File %s does not exist." % step
				return 2
		output_app(data)
	
	# TODO:
	# punct_point=`grep -nH ' real pilcrow' $PUNCTLEXC | cut -f2 -d':'`;
	# head -n $punct_point $PUNCTLEXC >> $OUTFILE;
	
	out_ = '\n'.join([a for a in output_])
	with open(OUTFILE, 'w') as F:
		F.write(out_)
	
	print '... Done.'
	print 'Saved to %s.\n' % OUTFILE
	return True


make_lexc()
