all:
	apertium-validate-dictionary apertium-sme-fin.sme-fin.dix
	lt-comp rl apertium-sme-fin.sme-fin.dix fin-sme.autobil.bin
