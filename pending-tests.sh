#!/bin/bash

C=2
GREP='.'
if [ $# -eq 1 ]
then
    C=$1
    GREP='WORKS'
fi

sh wiki-tests.sh Pending fin sme update | grep -C $C "$GREP"


