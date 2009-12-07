all:
	cat Adv.lex.orig | python calc-levenshtein.py | sort -ugr > Adv.lex
	cat A.lex.orig | python calc-levenshtein.py | sort -ugr > A.lex
	cat N.lex.orig | python calc-levenshtein.py | sort -ugr > N.lex
	cat N.Prop.lex.orig | python calc-levenshtein.py | sort -ugr > N.Prop.lex
	cat Po.lex.orig | python calc-levenshtein.py | sort -ugr > Po.lex
	cat Pron.lex.orig | python calc-levenshtein.py | sort -ugr > Pron.lex
	cat V.lex.orig | python calc-levenshtein.py | sort -ugr > V.lex

clean:
	rm *.lex;
