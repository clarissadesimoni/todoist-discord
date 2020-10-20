#!/bin/bash

cd "INSERT THE DIRECTORY WHERE YOU STORE THE FILE WITH INFO"
filename=`date +%Y%m%d`".txt"
for f in `date +%Y`*".txt"; do
    if [ -f $f ]; then
        if [ $f != $filename ]; then
            rm $f
        fi
    fi
done
if [ ! -f $filename ]; then
    > $filename
fi
python mytodoistAPI.py
