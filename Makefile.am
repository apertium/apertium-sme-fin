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
	$(PREFIX2).lrx.bin \
	$(PREFIX2).lex.bin \
	$(PREFIX1).autobil.bin \
	$(PREFIX2).autobil.bin \
	$(PREFIX2).t1x.bin \
	$(PREFIX2).t2x.bin \
	$(PREFIX2).t3x.bin \
	$(PREFIX1).automorf.hfst \
	$(PREFIX2).mode

# This include defines goals for install-modes, .deps/.d and .mode files:
@ap_include@


#
#
#

$(PREFIX2).automorf.hfst: $(AP_LIB2)/$(LANG2).automorf.hfst
	cp $(AP_LIB2)/$(LANG2).automorf.hfst $@

$(PREFIX1).autogen.hfst: $(AP_LIB2)/$(LANG2).autogen.hfst
	cp $(AP_LIB2)/$(LANG2).autogen.hfst $@

#
# This is a generator 'apertium-sme-smj.smj.hfst'
#

.deps/$(PREFIX1).autobil.prefixes: $(PREFIX1).autobil.bin .deps/.d
	lt-print $< | sed 's/ /@_SPACE_@/g' > .deps/$(PREFIX1).autobil.att
	hfst-txt2fst -e ε <  .deps/$(PREFIX1).autobil.att > .deps/$(PREFIX1).autobil.hfst
	hfst-project -p upper .deps/$(PREFIX1).autobil.hfst > .deps/$(PREFIX1).autobil.upper
	echo ' [ ? - %+ ]* ' | hfst-regexp2fst > .deps/any-nonplus.hfst
	hfst-concatenate -1 .deps/$(PREFIX1).autobil.upper -2 .deps/any-nonplus.hfst -o .deps/$(PREFIX1).autobil.nonplussed # bidix [^+]*
	echo ' %+ ' | hfst-regexp2fst > .deps/single-plus.hfst
	hfst-concatenate -1 .deps/single-plus.hfst -2 .deps/$(PREFIX1).autobil.nonplussed -o .deps/$(PREFIX1).autobil.postplus # + bidix [^+]*
	hfst-repeat -f0 -t1 -i .deps/$(PREFIX1).autobil.postplus -o .deps/$(PREFIX1).autobil.postplus.0,1 # (+ bidix [^+]*){0,1} gives at most one +
	hfst-concatenate -1 .deps/$(PREFIX1).autobil.nonplussed -2 .deps/$(PREFIX1).autobil.postplus.0,1 -o $@

#.deps/$(LANG1).automorf.hfst: $(AP_SRC1)/$(BASENAME).$(PREFIX1).LR.att.gz .deps/.d
.deps/$(LANG1).automorf.hfst: $(AP_SRC1)/apertium-sme-nob.sme-nob.LR.att.gz .deps/.d
	$(ZCAT) $< | hfst-txt2fst > $@

.deps/$(LANG1).autogen.hfst: $(AP_SRC1)/apertium-sme-nob.sme-nob.LR.att.gz .deps/.d
	$(ZCAT) $< | hfst-txt2fst | hfst-invert -o $@

.deps/$(PREFIX1).automorf-unrestricted.hfst: .deps/$(LANG1).automorf.hfst .deps/$(PREFIX1).autobil.prefixes
	hfst-compose-intersect -1 $< -2 .deps/$(PREFIX1).autobil.prefixes -o $@

$(PREFIX1).automorf-unrestricted.hfst: .deps/$(PREFIX1).automorf-unrestricted.hfst
	hfst-fst2fst -O -i $< -o $@

# rm-deriv-cmp.twol is checked in to SVN since derivation-tags.txt is
# not installed by giella-sme; this goal only run if --with-lang1 set
rm-deriv-cmp.twol: $(wildcard $(AP_SRC1)/filters/derivation-tags.txt*) dev/update-rm-deriv-cmp
	test "$<" = "$^" || dev/update-rm-deriv-cmp $< $@
# The wildcard+test means we ignore the goal if we don't find
# derivation-tags.txt

.deps/rm-deriv-cmp.hfst: rm-deriv-cmp.twol .deps/.d
	hfst-twolc -i $< -o $@

.deps/$(PREFIX1).automorf.hfst: .deps/$(PREFIX1).automorf-unrestricted.hfst .deps/rm-deriv-cmp.hfst
	hfst-compose-intersect -1 $< -2 .deps/rm-deriv-cmp.hfst -o $@

$(PREFIX1).automorf.hfst: .deps/$(PREFIX1).automorf.hfst
	hfst-fst2fst -O -i $< -o $@


$(PREFIX2).autogen.hfst: .deps/$(LANG1).autogen.hfst
	hfst-fst2fst -O -i $< -o $@


## 	BILINGUAL DICTIONARIES

$(PREFIX1).autobil.bin: $(BASENAME).$(PREFIX1).dix
	apertium-validate-dictionary $(BASENAME).$(PREFIX1).dix
	lt-comp lr $(BASENAME).$(PREFIX1).dix $@


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

$(PREFIX2).lrx.bin: $(BASENAME).$(PREFIX2).lrx
	lrx-comp $(BASENAME).$(PREFIX2).lrx $@


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
	$(PREFIX2).prob \
	$(BASENAME).$(PREFIX2).rlx \
	$(BASENAME).$(PREFIX2).lrx \
	$(BASENAME).$(PREFIX2).dix \
	$(BASENAME).$(PREFIX2).t1x \
	$(BASENAME).$(PREFIX2).t2x \
	$(BASENAME).$(PREFIX2).t3x \
	modes.xml 


apertium_sme_findir=$(prefix)/share/apertium/$(BASENAME)/
apertium_sme_modesdir=$(prefix)/share/apertium/modes/

apertium_sme_fin_DATA=$(TARGETS_COMMON)


install-data-local:
	mv modes modes.bak
	apertium-gen-modes modes.xml $(BASENAME)
	rm -rf modes
	mv modes.bak modes
	test -d $(DESTDIR)$(apertium_sme_modesdir) || mkdir $(DESTDIR)$(apertium_sme_modesdir)
	$(INSTALL_DATA) $(PREFIX2).mode $(DESTDIR)$(apertium_sme_modesdir)
	rm $(PREFIX2).mode
	$(INSTALL_DATA) $(BASENAME).$(PREFIX2).t1x $(DESTDIR)$(apertium_sme_findir)
	$(INSTALL_DATA) $(BASENAME).$(PREFIX2).t2x $(DESTDIR)$(apertium_sme_findir)
	$(INSTALL_DATA) $(BASENAME).$(PREFIX2).t3x $(DESTDIR)$(apertium_sme_findir)




CLEANFILES= -rf $(TARGETS_COMMON) .deps modes
