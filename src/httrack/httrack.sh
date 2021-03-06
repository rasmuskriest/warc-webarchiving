#!/bin/sh

url=$1
folder=$2
dir=$3

mkdir -p $dir

httrack $url \
    --mirror \
    --quiet \
    --debug-headers \
    -O "$folder" \
    --assume php3=text/html,php=text/html,php4=text/html,php2=text/html,cgi=text/html,asp=text/html,jsp=text/html,pl=text/html,cfm=text/html \
    -F "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36" \
    -a \
    --search-index \
    -s2 \
    -u2 \
    --max-rate=10000000 \
    -ad.doubleclick.net/* -mime:application/foobar +*.png +*.gif +*.jpg +*.jpeg +*.css +*.js +mime:text/html +mime:image/*
