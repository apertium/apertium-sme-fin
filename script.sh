OMORFI=$GTHOME/kt/fin/omorfi
FINCG=$GTHOME/kt/fin/src/fin-dis.bin

sed 's/\W/\n&\n/g' | grep -v '^ $' |\
hfst-lookup -f apertium $OMORFI/src/mor-omorfi.apertium.hfst |\
cg-proc $FINCG |\
apertium-tagger -g fin-sme.prob |\
apertium-transfer apertium-sme-fin.fin-sme.t1x fin-sme.t1x.bin fin-sme.autobil.bin
