DELIMITERS = "<$\.>" "<$!>" "<$?>" "<.>" "<!>" "<?>" "<...>" "<¶>" CLB;

SETS

LIST Gen = Gen;
LIST Ela = Ela;

LIST @SUBJ→ = @SUBJ→;
LIST @←SUBJ = @←SUBJ;
LIST @OBJ→ = @OBJ→;
LIST @←OBJ = @←OBJ;

LIST CLB = CLB;


# Word categories

LIST AIKA = "vuosi" "aika" "kuukausi" "tunti" "viikko" ;

SECTION

# pitää → 1: berret, 2: liikot, 3: coakcut

SUBSTITUTE ("pitää") ("pitää:1") ("pitää" V) ((-1* @SUBJ→ + Gen BARRIER CLB) OR (1* @←SUBJ + Gen BARRIER CLB));
SUBSTITUTE ("pitää") ("pitää:2") ("pitää" V) ((1* Ela BARRIER CLB) OR (-1* Ela BARRIER CLB));

# käydä = fitnat. 1: fallehit
SUBSTITUTE ("käydä") ("käydä:1") ("käydä" V) (1* ("kimppuun") BARRIER CLB);

# vaihde = molsa. 1: jorggáldat
# SUBSTITUTE ("vaihde") ("vaihde:1") ("vaihde" N) (-1 AIKA);



#    <e><p><l>doallat<s n="V"/><s n="TV"/></l><r>pitää<s n="V"/></r></p><par n="V_V"/></e><!-- hold (acc) -->
#    <e srl="1"><p><l>berret<s n="V"/><s n="IV"/></l><r>pitää<s n="V"/></r></p><par n="V_V"/></e><!-- burde, ought to -->
#    <e srl="2"><p><l>liikot<s n="V"/><s n="IV"/></l><r>pitää<s n="V"/></r></p><par n="V_V"/></e><!-- like (ela to ill)  -->
#    <e srl="3"><p><l>coakcut<s n="V"/><s n="IV"/></l><r>pitää<s n="V"/></r></p><par n="V_V"/></e><!-- get grip, foothold -->

