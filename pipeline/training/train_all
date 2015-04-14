#!/bin/bash

if test "$#" -ne 2; then
    echo "Illegal number of parameters. Usage: bash trial.sh [PATH-TO-GROBID] [PATH-TO-LOG-FOLDER]"
else
    declare -a models=("affiliation" "chemical" "date" "citation" "ebook" \
                "fulltext" "header" "name-citation" "name-header" \
                "patent" "segmentation" "reference-segmenter")

    for i in "${models[@]}"
    do
        java -Xmx1024m -jar $1"grobid/grobid-trainer/target/grobid-trainer.jar" "2" "$i" "-gH" "grobid/grobid-home" "-s" "0.8" > $2/"$i".log
    done
fi
