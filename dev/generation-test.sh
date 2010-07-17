BIBLE=/home/fran/corpora/finnish/bible.fi/*.txt

if [[ $1 == "-r" ]]; then
	echo -n "Processing corpus for generation test (this could take some time)... ";
	cat $BIBLE | apertium -d ../ fin-sme-postchunk | sed 's/\$\W*\^/$\n^/g' > /tmp/fin.gentest.postchunk
	echo "done.";
fi

if [[ ! -f /tmp/fin.gentest.postchunk ]]; then
	echo "Something went wrong in processing the corpus, you have no output file.";
	echo "Try running:"
	echo "   sh generation-test.sh -r";
	exit;
fi

cat /tmp/fin.gentest.postchunk  | sed 's/^ //g' | grep -v -e '@' -e '*' -e '[0-9]<Num>' | sed 's/\$>/$/g' | sort -f | uniq -c | sort -gr > /tmp/fin.gentest.stripped
cat /tmp/fin.gentest.stripped | hfst-proc -g ../fin-sme.autogen.hfst > /tmp/fin.gentest.surface
cat /tmp/fin.gentest.stripped | sed 's/^ *[0-9]* \^/^/g' > /tmp/fin.gentest.nofreq
paste /tmp/fin.gentest.surface /tmp/fin.gentest.nofreq | grep -e '\/' -e '#'  > /tmp/fin.generation.errors.txt
cat /tmp/fin.generation.errors.txt  | grep -v '#' | grep '\/' > /tmp/fin-sme.multiform
cat /tmp/fin.generation.errors.txt  | grep '#.*\/' > /tmp/fin-sme.multibidix 
cat /tmp/fin.generation.errors.txt  | grep '#' | grep -v '\/' > /tmp/fin-sme.tagmismatch 

echo "";
echo "===============================================================================";
echo "Multiple surface forms for a single lexical form";
echo "===============================================================================";
cat /tmp/fin-sme.multiform

echo "";
echo "===============================================================================";
echo "Multiple bidix entries for a single source language lexical form";
echo "===============================================================================";
cat /tmp/fin-sme.multibidix

echo "";
echo "===============================================================================";
echo "Tag mismatch between transfer and generation";
echo "===============================================================================";
cat /tmp/fin-sme.tagmismatch

echo "";
echo "===============================================================================";
echo "Summary";
echo "===============================================================================";
wc -l /tmp/fin-sme.multiform /tmp/fin-sme.multibidix /tmp/fin-sme.tagmismatch
