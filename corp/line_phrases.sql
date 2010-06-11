-- Usage: cat line_phrases.sql | sqlite3
-- Ensure that fi.db and se.db are all in the same dir.
-- Fetch data from: http://open-tran.eu/dev.html

ATTACH DATABASE "fi.db" as fi;
ATTACH DATABASE "se.db" as se;

.mode csv
-- .output open_tran_-_fin_sme.txt
select sep.phrase, fip.phrase from se.phrases as sep, fi.phrases as fip where sep.id=fip.id;
