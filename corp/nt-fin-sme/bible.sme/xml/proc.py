#!/usr/bin/python2.5
# coding=utf-8
# -*- encoding: utf-8 -*-

import sys, codecs, copy;

sys.stdout = codecs.getwriter('utf-8')(sys.stdout);
sys.stderr = codecs.getwriter('utf-8')(sys.stderr);

book = 39;
chapter = 0;
verse = 0;
out = '';
for line in sys.stdin.read().split('\n'): #{
	
	if line.count('<book title="') > 0: #{
		book = book + 1;
		verse = 0;
		chapter = 0;
	#}
	if line.count('<chapter') > 0: #{
		chapter = chapter + 1;
	#}
	if line.count('</chapter>') > 0: #{
		fn = '../book%03d.chapter%03d.txt' % (int(book), int(chapter));
		f = open(fn, 'w+');
		print book , chapter , fn;
		print >> f , out.strip();
		f.close();
		out = '';
		verse = 0;
	#}
	if line.count('<verse') > 0: #{
#66 22 18           <verse number="18"> Mun duođaštan juohkehažžii guhte gullá dán girjji profehtalaš sániid: Jos giige lasiha maidege, de Ipmil bidjá su ala daid givssiid maid birra dán girjjis lea čállojuvvon. </verse>
		out = out + line.replace('<verse number="', '').replace('</verse>','').replace('">','\t').strip() + '\n'; 
	#}

#}
