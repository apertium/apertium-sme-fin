all:
	apertium-validate-dictionary apertium-sme-fin.sme-fin.dix
	lt-comp rl apertium-sme-fin.sme-fin.dix fin-sme.autobil.bin

	apertium-validate-transfer apertium-sme-fin.fin-sme.t1x
	apertium-preprocess-transfer apertium-sme-fin.fin-sme.t1x fin-sme.t1x.bin
