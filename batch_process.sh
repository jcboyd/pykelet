#!/bin/bash

# Convert pdf files to text files
if [ "$1" = "all" ] || [ "$1" = "convert" ]
	then
		for PATHNAME in input-pdf/*.pdf
		do
			echo "Converting $PATHNAME"
			python pre_process.py $PATHNAME
		done
fi

# Run ParsCit on raw text
if [ "$1" = "all" ] || [ "$1" = "tag" ] || [ "$1" = "parscit" ]
	then
		for PATHNAME in input-text/*.txt
		do
			echo "Tagging $PATHNAME"
			FILENAME="${PATHNAME##*/}"
			FILENAME="${FILENAME%.*}"
			parscit/bin/citeExtract.pl -m extract_all $PATHNAME output-parscit/$FILENAME".xml"
		done
fi

if [ "$1" = "all" ] || [ "$1" = "tag" ] || [ "$1" = "grobid" ]
	then
		java -Xmx1024m -jar grobid/grobid-core/target/grobid-core-0.3.3-SNAPSHOT.one-jar.jar -gH grobid/grobid-home -gP /grobid/grobid-home/config/grobid.properties -dIn input-pdf/ -dOut output-grobid/ -exe processFullText
fi