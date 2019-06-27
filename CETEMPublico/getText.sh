#!/bin/bash
for  file  in  *.txt; do
     gawk -f convert.awk "$file" > "${file%.utf8.txt}.txt"
done
exit 0
