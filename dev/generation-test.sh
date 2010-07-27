#!/bin/bash

if [[ $# -lt 2 ]]; then
	echo "Not enough arguments to generation-test.sh -r";
	echo "bash generation-test.sh -r <corpus>";
	exit;
fi

if [[ $1 == "-r" ]]; then
	if [[ $# -lt 2 ]]; then 
		echo $#;
		echo "Not enough arguments to generation-test.sh -r";
		echo "bash generation-test.sh -r <corpus>";
		exit;
	fi
	args=("$@")
	echo "Corpus in: "`dirname $2`;
	echo -n "Processing corpus for generation test... ";
	rm -f /tmp/fin-sme.corpus.txt
	for i in `seq 1 $#`; do 
		if [[ ${args[$i]} != "" && -f ${args[$i]} ]]; then 
			cat ${args[$i]} >> /tmp/fin-sme.corpus.txt
		fi
	done
	echo "done.";
	echo -n "Translating corpus for generation test (this could take some time)... ";
	cat /tmp/fin-sme.corpus.txt | apertium -d ../ fin-sme-postchunk | sed 's/\$\W*\^/$\n^/g' > /tmp/fin.gentest.postchunk
	echo "done.";
fi

if [[ ! -f /tmp/fin.gentest.postchunk ]]; then
	echo "Something went wrong in processing the corpus, you have no output file.";
	echo "Try running:"
	echo "   sh generation-test.sh -r <corpus>";
	exit;
fi

cat /tmp/fin.gentest.postchunk  | sed 's/^ //g' | grep -v -e '@' -e '*' -e '[0-9]<Num>' -e '#}' -e '#{' | sed 's/\$>/$/g' | sort -f | uniq -c | sort -gr > /tmp/fin.gentest.stripped
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
