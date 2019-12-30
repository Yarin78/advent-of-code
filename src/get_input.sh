#!/bin/bash
if [ $# -ne 3 ]; then
    echo 'Usage: get_input <year> <day> <session>'
    exit 1
fi
if [ $1 -lt 2015 ]; then
    echo 'Invalid year'
    exit 1
fi
if [ $2 -gt 25 ]; then
    echo 'Invalid day'
    exit 1
fi
curl https://adventofcode.com/$1/day/$2/input --cookie "session=$3" > year$1/day$2.in
