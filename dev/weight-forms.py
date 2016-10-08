import sys
import kenlm

LM = sys.argv[1];
model = kenlm.LanguageModel(LM)

offset = 0.001;
for line in sys.stdin.readlines(): #{
	row = line.strip('\n').split('/');
	
	total = 0.0;
	for w in row: #{
		total = total + model.score(w);	
	#}
	first = True;	
	for w in row: #{
		score = 0.0
		if first: #{
			score = 1.0-(((model.score(w))/total)+offset);
		else: #{
			score = 1.0-(model.score(w)/total)

		#}
		print('%.2f\t%s' % (score, w));
		first = False;
	#}
#}
