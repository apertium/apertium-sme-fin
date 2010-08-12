DELIMITERS = "<$\.>" "<$!>" "<$?>" "<.>" "<!>" "<?>" "<...>" "<¶>" CLB;

SETS

LIST Gen = Gen;
LIST Ela = Ela;

LIST @SUBJ→ = @SUBJ→;
LIST @←SUBJ = @←SUBJ;
LIST @OBJ→ = @OBJ→;
LIST @←OBJ = @←OBJ;

LIST CLB = CLB;


SECTION

# pitää → 1: berret, 2: liikot, 3: coakcut

SUBSTITUTE ("pitää") ("pitää:1") ("pitää" V) ((-1* @SUBJ→ + Gen BARRIER CLB) OR (1* @←SUBJ + Gen BARRIER CLB));
SUBSTITUTE ("pitää") ("pitää:2") ("pitää" V) ((1* @←OBJ + Ela BARRIER CLB) OR (-1* @OBJ→ + Ela BARRIER CLB));
