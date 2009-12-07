all:
	cat Adv.lex.orig | python calc-levenshtein.py | sort -u | sort -gr > Adv.lex
	cat A.lex.orig | python calc-levenshtein.py | sort -u | sort -gr > A.lex
	cat N.lex.orig | python calc-levenshtein.py | sort -u | sort -gr > N.lex
	cat N.Prop.lex.orig | python calc-levenshtein.py | sort -u | sort -gr > N.Prop.lex
	cat Po.lex.orig | python calc-levenshtein.py | sort -u | sort -gr > Po.lex
	cat Pron.lex.orig | python calc-levenshtein.py | sort -u | sort -gr > Pron.lex
	cat V.lex.orig | python calc-levenshtein.py | sort -u | sort -gr > V.lex
	cat Conj.lex.orig | python calc-levenshtein.py | sort -u | sort -gr > Conj.lex

clean:
	rm *.lex;
