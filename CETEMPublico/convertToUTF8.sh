#!/bin/bash

FROM_ENCODING="ISO-8859-1"
TO_ENCODING="UTF-8"
CONVERT="iconv -f $FROM_ENCODING -t $TO_ENCODING"

for  file  in  *.txt; do
     $CONVERT   "$file"   -o  "${file%.txt}.utf8.txt"
done
exit 0
