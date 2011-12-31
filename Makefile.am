VERSION=0.1.0
LANG1=sme
LANG2=fin
PREFIX1=$(LANG1)-$(LANG2)
PREFIX2=$(LANG2)-$(LANG1)

BASENAME=apertium-$(PREFIX1)

##
##	BUILD TARGETS
##

TARGETS_COMMON = \
	$(PREFIX2).autogen.hfst \
	$(PREFIX2).automorf.hfst \
	$(PREFIX2).rlx.bin \
	$(PREFIX2).lex.bin \
	$(PREFIX2).autobil.bin \
	$(PREFIX2).t1x.bin \
	$(PREFIX2).t2x.bin \
	$(PREFIX2).t3x.bin \
	$(PREFIX1).automorf.hfst \
	$(PREFIX2).mode

##
## 	ANALYSER / GENERATOR / POSTGEN DICTIONARIES
##

.deps/$(LANG1).twol.hfst: $(BASENAME).$(LANG1).twol
	if [ ! -d .deps ]; then mkdir .deps; fi
	hfst-twolc -R -i $(BASENAME).$(LANG1).twol -o $@

.deps/$(LANG1).lexc.hfst: $(BASENAME).$(LANG1).lexc
	if [ ! -d .deps ]; then mkdir .deps; fi
	hfst-lexc $(BASENAME).$(LANG1).lexc -o $@

.deps/$(LANG2).twol.hfst: $(BASENAME).$(LANG2).twol
	if [ ! -d .deps ]; then mkdir .deps; fi
	hfst-twolc -R -i $(BASENAME).$(LANG2).twol -o $@

.deps/$(LANG2).lexc.hfst: $(BASENAME).$(LANG2).lexc
	if [ ! -d .deps ]; then mkdir .deps; fi
	hfst-lexc $(BASENAME).$(LANG2).lexc -o $@

#
# These are scripts that remove unwanted tags
#
.deps/xfst2apertium.useless.generation.twol.hfst: dev/xfst2apertium.useless.generation.twol
	if [ ! -d .deps ]; then mkdir .deps; fi
	hfst-twolc -R -i dev/xfst2apertium.useless.generation.twol -o $@

.deps/xfst2apertium.useless.analysis.twol.hfst: dev/xfst2apertium.useless.analysis.twol
	if [ ! -d .deps ]; then mkdir .deps; fi
	hfst-twolc -R -i dev/xfst2apertium.useless.analysis.twol -o $@

.deps/xfst2apertium.hashtags.twol.hfst: dev/xfst2apertium.hashtags.twol
	if [ ! -d .deps ]; then mkdir .deps; fi
	hfst-twolc -R -i dev/xfst2apertium.hashtags.twol -o $@

#
# This is a generator 'apertium-sme-smj.fin.hfst'
#
.deps/$(BASENAME).$(LANG2).hfst: .deps/$(LANG2).lexc.hfst .deps/$(LANG2).twol.hfst
	if [ ! -d .deps ]; then mkdir .deps; fi
	hfst-compose-intersect -1 .deps/$(LANG2).lexc.hfst -2 .deps/$(LANG2).twol.hfst -o $@

# apertium-sme-fin , fin-sme , fin
.deps/$(PREFIX2).automorf.hfst: .deps/$(BASENAME).$(LANG2).hfst dev/omorfi2apertium.relabel
	if [ ! -d .deps ]; then mkdir .deps; fi
	hfst-invert .deps/$(BASENAME).$(LANG2).hfst -o .deps/$(PREFIX2).automorf.hfst.tmp
	hfst-substitute -F dev/omorfi2apertium.relabel -i .deps/$(PREFIX2).automorf.hfst.tmp -o .deps/$(PREFIX2).automorf.hfst

$(PREFIX2).automorf.hfst: .deps/$(PREFIX2).automorf.hfst
	hfst-fst2fst -O -i  .deps/$(PREFIX2).automorf.hfst -o $@ # should it be .ol for -o file?

$(PREFIX1).autogen.hfst: .deps/$(PREFIX1).automorf.hfst
	hfst-fst2fst -O -i  .deps/$(PREFIX1).autogen.hfst -o $@ # should it be .ol for -o file?

#
# This is a generator 'apertium-sme-smj.smj.hfst'
#
.deps/$(BASENAME).$(LANG1).hfst: .deps/$(LANG1).lexc.hfst .deps/$(LANG1).twol.hfst
	if [ ! -d .deps ]; then mkdir .deps; fi
	hfst-compose-intersect -1 .deps/$(LANG1).lexc.hfst -2 .deps/$(LANG1).twol.hfst -o $@

.deps/$(PREFIX2).autogen.hfst: .deps/$(BASENAME).$(LANG1).hfst .deps/xfst2apertium.useless.generation.twol.hfst .deps/xfst2apertium.hashtags.twol.hfst dev/xfst2apertium.relabel
	if [ ! -d .deps ]; then mkdir .deps; fi
	hfst-invert .deps/$(BASENAME).$(LANG1).hfst -o .deps/$(PREFIX1).automorf.orig.tmp
	hfst-compose-intersect -1 .deps/$(PREFIX1).automorf.orig.tmp -2 .deps/xfst2apertium.useless.generation.twol.hfst -o .deps/$(PREFIX1).automorf.useless.tmp
	hfst-compose-intersect -1 .deps/$(PREFIX1).automorf.useless.tmp -2 .deps/xfst2apertium.hashtags.twol.hfst -o .deps/$(PREFIX1).automorf.hashtags.tmp
	hfst-invert .deps/$(PREFIX1).automorf.hashtags.tmp -o .deps/$(PREFIX2).autogen.hashtags.tmp
	hfst-substitute -F dev/xfst2apertium.relabel -i .deps/$(PREFIX2).autogen.hashtags.tmp -o .deps/$(PREFIX2).autogen.hfst

#	rm .deps/$(PREFIX1).automorf.orig.tmp .deps/$(PREFIX1).automorf.useless.tmp .deps/$(PREFIX1).automorf.hashtags.tmp .deps/$(PREFIX2).autogen.hashtags.tmp

$(PREFIX2).autogen.hfst: .deps/$(PREFIX2).autogen.hfst
	hfst-fst2fst -O -i  .deps/$(PREFIX2).autogen.hfst -o $@ # should it be .ol for -o file?

$(PREFIX1).automorf.hfst: .deps/$(PREFIX2).autogen.hfst
	if [ ! -d .deps ]; then mkdir .deps; fi
	hfst-invert .deps/$(PREFIX2).autogen.hfst -o .deps/$(PREFIX1).automorf.hfst
	hfst-fst2fst -O -i  .deps/$(PREFIX1).automorf.hfst -o $@ # should it be .ol for -o file?


## 	BILINGUAL DICTIONARIES

#.deps/$(BASENAME).$(PREFIX1).dix: $(BASENAME).$(PREFIX1).dix lexchoicebil.xsl
#	if [ ! -d .deps ]; then mkdir .deps; fi
#	xsltproc lexchoicebil.xsl $(BASENAME).$(PREFIX1).dix > $@

$(PREFIX2).autobil.bin: $(BASENAME).$(PREFIX1).dix
	apertium-validate-dictionary $(BASENAME).$(PREFIX1).dix
	lt-comp rl $(BASENAME).$(PREFIX1).dix $@

##
##	PRE-TAGGING: CONSTRAINT GRAMMAR(S)
##

$(PREFIX2).rlx.bin: $(BASENAME).$(PREFIX2).rlx
	cg-comp $(BASENAME).$(PREFIX2).rlx $@

##
##	LEXICAL SELECTION: CONSTRAINT GRAMMAR(S)
##

$(PREFIX2).lex.bin: $(BASENAME).$(PREFIX2).lex
	cg-comp $(BASENAME).$(PREFIX2).lex $@

##
##	TRANSFER RULES
##

$(PREFIX2).t1x.bin: $(BASENAME).$(PREFIX2).t1x
	apertium-validate-transfer $(BASENAME).$(PREFIX2).t1x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX2).t1x $@

$(PREFIX2).t2x.bin: $(BASENAME).$(PREFIX2).t2x
	apertium-validate-interchunk $(BASENAME).$(PREFIX2).t2x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX2).t2x $@

$(PREFIX2).t3x.bin: $(BASENAME).$(PREFIX2).t3x
	apertium-validate-postchunk $(BASENAME).$(PREFIX2).t3x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX2).t3x $@



##
##	MODE FILE(S)
##

$(PREFIX2).mode: modes.xml
	apertium-validate-modes modes.xml
	apertium-gen-modes modes.xml
	cp *.mode modes/

# So that debug modes get built even if we don't "make install":
noinst_DATA=modes/$(PREFIX2).mode

## 
##	FILES WHICH AREN'T BUILT BUT ARE DISTRIBUTED
## 

EXTRA_DIST=\
	$(BASENAME).$(LANG1).twol \
	$(BASENAME).$(LANG1).lexc \
	$(BASENAME).$(PREFIX2).rlx \
	$(BASENAME).$(PREFIX2).dix \
	$(BASENAME).$(LANG2).twol \
	$(BASENAME).$(LANG2).lexc \
	$(BASENAME).$(PREFIX2).t1x \
	$(BASENAME).$(PREFIX2).t2x \
	$(BASENAME).$(PREFIX2).t3x \
	modes.xml 


apertium_sme_findir=$(prefix)/share/apertium/$(BASENAME)/
apertium_sme_modesdir=$(prefix)/share/apertium/modes/

apertium_sme_fin_DATA=$(TARGETS_COMMON)


CLEANFILES= -rf $(TARGETS_COMMON) .deps modes
