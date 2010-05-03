OMORFI=/home/fran/source/giellatekno/trunk/kt/fin/omorfi
FINCG=/home/fran/source/giellatekno/trunk/kt/fin/src/fin-dis.bin

sed 's/\W/\n&\n/g' | grep -v '^ $' |\
hfst-lookup -f apertium $OMORFI/src/mor-omorfi.apertium.hfst |\
cg-proc $FINCG
