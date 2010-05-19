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
	$(PREFIX2).rlx.bin \
	$(PREFIX2).autobil.bin \
	$(PREFIX2).t1x.bin \
	$(PREFIX2).mode

##
## 	ANALYSER / GENERATOR / POSTGEN DICTIONARIES
##

$(LANG1).twol.hfst: $(BASENAME).$(LANG1).twol
	hfst-twolc -r -i $(BASENAME).$(LANG1).twol -o $@

$(LANG1).lexc.hfst: $(BASENAME).$(LANG1).lexc
	hfst-lexc $(BASENAME).$(LANG1).lexc -o $@

$(PREFIX2).autogen.hfst: $(LANG1).twol.hfst $(LANG1).lexc.hfst .deps/uppercase-first.twol.hfst
	hfst-compose-intersect -l $(LANG1).lexc.hfst $(LANG1).twol.hfst -o $@.tmp
	hfst-substitute -F dev/xfst2apertium.relabel -i $@.tmp -o $@

.deps/uppercase-first.twol.hfst: dev/uppercase-first.twol
	if [ ! -d .deps ]; then mkdir .deps; fi
	hfst-twolc -r -i dev/uppercase-first.twol -o $@


.deps/xfst2apertium.useless.twol.hfst: dev/xfst2apertium.useless.twol
	if [ ! -d .deps ]; then mkdir .deps; fi
	hfst-twolc -r -i dev/xfst2apertium.useless.twol -o $@

.deps/xfst2apertium.hashtags.twol.hfst: dev/xfst2apertium.hashtags.twol
	if [ ! -d .deps ]; then mkdir .deps; fi
	hfst-twolc -r -i dev/xfst2apertium.hashtags.twol -o $@

$(PREFIX1).automorf.hfst: $(PREFIX2).autogen.hfst dev/xfst2apertium.relabel .deps/xfst2apertium.useless.twol.hfst .deps/xfst2apertium.hashtags.twol.hfst
	hfst-invert $(PREFIX2).autogen.hfst -o $@.1.tmp
	hfst-compose-intersect -l $@.1.tmp .deps/xfst2apertium.useless.twol.hfst -o $@.2.tmp
	hfst-compose-intersect -l $@.2.tmp .deps/xfst2apertium.hashtags.twol.hfst -o $@.3.tmp
	hfst-substitute -F dev/xfst2apertium.relabel -i $@.3.tmp -o $@

#	@rm $@.1.tmp $@.2.tmp $@.3.tmp

## 	BILINGUAL DICTIONARIES

.deps/$(BASENAME).$(PREFIX1).dix: $(BASENAME).$(PREFIX1).dix lexchoicebil.xsl
	if [ ! -d .deps ]; then mkdir .deps; fi
	xsltproc lexchoicebil.xsl $(BASENAME).$(PREFIX1).dix > $@

$(PREFIX2).autobil.bin: .deps/$(BASENAME).$(PREFIX1).dix
	apertium-validate-dictionary .deps/$(BASENAME).$(PREFIX1).dix
	lt-comp rl .deps/$(BASENAME).$(PREFIX1).dix $@

##
##	PRE-TAGGING
##

$(PREFIX2).rlx.bin: $(BASENAME).$(PREFIX2).rlx
	cg-comp $(BASENAME).$(PREFIX2).rlx $@

##
##	TRANSFER RULES
##

$(PREFIX2).t1x.bin: $(BASENAME).$(PREFIX2).t1x
	apertium-validate-transfer $(BASENAME).$(PREFIX2).t1x
	apertium-preprocess-transfer $(BASENAME).$(PREFIX2).t1x $@

#
#	MODE FILE(S)
#

$(PREFIX2).mode: modes.xml
	apertium-validate-modes modes.xml
	apertium-gen-modes modes.xml
	cp *.mode modes/

## 
##	FILES WHICH AREN'T BUILD BUT ARE DISTRIBUTED
## 

EXTRA_DIST=\
	$(BASENAME).$(LANG1).twol \
	$(BASENAME).$(LANG1).lexc \
	$(BASENAME).$(PREFIX2).rlx \
	$(BASENAME).$(PREFIX2).dix \
	$(BASENAME).$(LANG2).twol \
	$(BASENAME).$(LANG2).lexc \
	$(BASENAME).$(PREFIX2).t1x \
	modes.xml 


apertium_sme_findir=$(prefix)/share/apertium/$(BASENAME)/
apertium_sme_modesdir=$(prefix)/share/apertium/modes/

apertium_sme_fin_DATA=$(TARGETS_COMMON)


CLEANFILES= -rf $(TARGETS_COMMON) .deps modes
