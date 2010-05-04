all:
	apertium-validate-dictionary apertium-sme-fin.sme-fin.dix
	lt-comp rl apertium-sme-fin.sme-fin.dix fin-sme.autobil.bin

	apertium-validate-transfer apertium-sme-fin.fin-sme.t1x
	apertium-preprocess-transfer apertium-sme-fin.fin-sme.t1x fin-sme.t1x.bin
	
	hfst-lexc apertium-sme-fin.sme.lexc -o sme.lexc.hfst
	hfst-twolc apertium-sme-fin.sme.twol -o sme.twol.hfst
	hfst-compose-intersect -l sme.lexc.hfst sme.twol.hfst -o sme.gen.hfst
	hfst-substitute -F dev/xfst2apertium.relabel sme.gen.hfst -o sme-fin.gen.hfst
