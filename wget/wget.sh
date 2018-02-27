#!/bin/sh

url=$1
dir=$2

mkdir -p $dir

wget $url \
    --recursive \
    --mirror \
    --warc-file="$dir/$url" \
    --warc-cdx \
    --page-requisites \
    --html-extension \
    --convert-links \
    --execute robots=off \
    --directory-prefix=. \
    --span-hosts \
    --domains=$url \
    --user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36"\
    --wait=1 \
    --random-wait \
    --append-output="$dir/$url".log
