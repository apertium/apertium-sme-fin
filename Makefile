all:
	xsltproc lexchoicebil.xsl apertium-sme-fin.sme-fin.dix > apertium-sme-fin.sme-fin.dix.tmp
	lt-comp rl apertium-sme-fin.sme-fin.dix.tmp fin-sme.autobil.bin
	rm apertium-sme-fin.sme-fin.dix.tmp

	apertium-validate-transfer apertium-sme-fin.fin-sme.t1x
	apertium-preprocess-transfer apertium-sme-fin.fin-sme.t1x fin-sme.t1x.bin
	
	hfst-lexc apertium-sme-fin.sme.lexc -o sme.lexc.hfst
#	Work out how to do this for generation -- it works for analysis
#	hfst-twolc -r -i dev/uppercase-first.twol -o dev/uppercase-first.hfst
#	hfst-compose-intersect -l sme.lexc.hfst.tmp dev/uppercase-first.hfst -o sme.lexc.hfst
	hfst-twolc apertium-sme-fin.sme.twol -o sme.twol.hfst
	hfst-compose-intersect -l sme.lexc.hfst sme.twol.hfst -o sme.gen.hfst
	hfst-substitute -F dev/xfst2apertium.relabel sme.gen.hfst -o fin-sme.autogen.hfst
	hfst-invert fin-sme.autogen.hfst -o sme-fin.automorf.hfst

	apertium-gen-modes modes.xml
