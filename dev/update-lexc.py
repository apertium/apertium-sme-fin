#!/usr/bin/python

import os
import sys
import subprocess as sp
import re

PIPE = sp.PIPE

# Global variables
TL = "sme"
SL = "fin"
PREFIX1 = "%s-%s" % (TL, SL)
BASENAME = "apertium-" + PREFIX1
GTHOME = os.environ.get("GTHOME")

if not GTHOME:
	print "$GTHOME not set."
	sys.exit() # TODO: exit with error

SRC = "%s/gt/%s/src" % (GTHOME, TL)

DEV = os.getcwd()
OUTFILE = "%s.%s.lexc" % (BASENAME, TL) # TODO: change to prod.


def lt_exp():
	"""docstring for init"""
	cmd = "lt-expand %s/../%s.%s.dix" % (DEV, BASENAME, PREFIX1) # TODO: generalize
	ltexp = sp.Popen(cmd.split(' '), shell=False, stdout=PIPE, stderr=PIPE, stdin=PIPE)
	output = ltexp.communicate()[0].split('\n')
	return output


def lex_header():
	"""
		Searches through lang-lex.txt and returns data, excluding certain lines.
		
		Returns a list for now.
	"""
	lex_excludes = [
		'\!\^NG\^',
		'; \!SUB', # '; !SUB',
		'\! \!SOUTH',
		'\+Use\/NG',
		'\+Nom(.*)\+Use\/Sub', # '+Nom.*+Use/Sub',
		'\+Gen(.*)\+Use\/Sub',
		'\+Use\/Sub(.*)\+V\+TV',
		'\+Attr(.*)\+Use\/Sub',
		'LEXICON PRSPRCTOADJ \!SUB',
		'\+Imprt(.*)\+Use\/Sub'	
	]
	
	# Compile regexp to exclude these items
	excl = re.compile(r'|'.join(['(?:' + a + ')' for a in lex_excludes]))
	
	lex_f = '%s/%s-lex.txt' % (SRC, TL)
	with open(lex_f, 'r') as F:
		lines = F.readlines()
		lex = [a for a in lines if not excl.search(a)]
	
	return lex
	


def extract(data, f_pos, s_pos, pos, split, no_header=False, debug=False):
	"""
		Given a full pos (f_pos), e.g., 'Verb', 'Noun' and PoS (pos), e.g. 'V', 'N'; extract these lines 
	"""
	
	fname = "%s/%s-%s-lex.txt" % ((SRC, s_pos, TL))
	
	if pos:
		search_key = '<' + pos
	else:
		search_key = False
		
	# Words matching pos
	if search_key:
		words = list(set([a.split('<')[0] for a in data if a.find(search_key) > -1]))
	else:
		words = list(set([a.split('<')[0] for a in data]))
	
	if debug:
		print str(len(words)) + ' unique words %s in .dix' % f_pos.lower()
	
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
	
	# remove silly symbols
	rest = rest.split('\n')
	# rest = [a for a in rest if not a.startswith('!')]
	
	# if this is slow, there is still something creative that can be done here
	stripchar = lambda x: x.replace('0','').replace('^','').replace('#','').split(':')[0].split('+')[0]
	
	trim = [a for a in rest if stripchar(a) in words]
	trim = '\n'.join(trim)

	if no_header:
		return '\n', point + '\n' + trim
	else:
		return head, trim


data = lt_exp()

# remove rexp lines and empty lines
lt_expand_data = [l for l in data if "REGEX" not in l and l.strip()]

header = lex_header()

# Use dicts for default behavior
# strings for just reading a filename with no action taken
# tuples with dict as first item and options as second

STEPS = [
	{'f_pos': 'Verb', 's_pos': 'verb', 'pos': 'V', 'split': 'VerbRoot\n'},
	{'f_pos': 'Noun', 's_pos': 'noun', 'pos': 'N', 'split': 'NounRoot\n'},
	{'f_pos': 'Adjective', 's_pos': 'adj', 'pos': 'A', 'split': 'AdjectiveRoot\n'},
	"%s/propernoun-%s-morph.txt" % ((SRC, TL)),
	{'f_pos': 'ProperNoun', 's_pos': 'propernoun', 'pos': 'N><Prop', 'split': 'ProperNoun\n'},
	"%s/conjunction-%s-lex.txt" % (SRC, TL),
	{'f_pos': 'Adverb', 's_pos': 'adv', 'pos': 'Adv', 'split': 'Adverb'},
	{'f_pos': 'Adverb', 's_pos': 'adv', 'pos': 'Adv', 'split': 'gadv ! adv that can form compounds', 'no_header': True},
	"%s/subjunction-%s-lex.txt" % (SRC, TL),
	"%s/pronoun-%s-lex.txt" % (SRC, TL),
	"%s/particle-%s-lex.txt" % (SRC, TL),
	"%s/pp-%s-lex.txt" % (SRC, TL),
	"%s/numeral-%s-lex.txt" % (SRC, TL),
	"%s/abbr-%s-lex.txt" % (SRC, TL),
	"%s/punct-%s-lex.txt" % (SRC, TL)
	# {'f_pos': 'Punctuation', 's_pos': 'punct', 'pos': False, 'split': 'real pilcrow\n'},
]

output_ = [''.join(header)]
for step in STEPS:
	if type(step) == dict:
		print "... Trimming %ss" % step['f_pos']
		head, trim = extract(lt_expand_data, **step)
		data = head + trim
	# elif type(step) == tuple:
	# 	head, trim = extract(lt_expand_data, **step[0])
	# 	print trim
	# 	if step[1].has_key('no_header'):
	# 		data = trim
	# 	else:
	# 		data = head + trim
	elif type(step) == str:
		with open(step, 'r') as F:
			print "... Reading %s" % step
			data = F.read()
	
	output_.append(data)


 


	# TODO:
	# punct_point=`grep -nH ' real pilcrow' $PUNCTLEXC | cut -f2 -d':'`;
	# head -n $punct_point $PUNCTLEXC >> $OUTFILE;

# out_ = ''.join(header) + '\n'.join([item['data'] for item in output_])

out_ = '\n'.join([a for a in output_])
with open(OUTFILE, 'w') as F:
	F.write(out_)

print '... Done.'
print 'Saved to %s.\n' % OUTFILE

# print data
