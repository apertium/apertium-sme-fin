if [[ !$GTHOME ]]; then
	GTHOME=/home/fran/source/giellatekno/trunk
fi

OMORFI=$GTHOME/kt/fin/omorfi
FINCG=$GTHOME/kt/fin/src/fin-dis.bin

hfst-proc $OMORFI/src/mor-omorfi.apertium.hfst |\
cg-proc -w $FINCG |\
apertium-tagger -g fin-sme.prob |\
apertium-transfer apertium-sme-fin.fin-sme.t1x fin-sme.t1x.bin fin-sme.autobil.bin |\
hfst-proc -g fin-sme.autogen.hfst
