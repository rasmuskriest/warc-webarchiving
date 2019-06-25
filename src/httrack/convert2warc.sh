#!/bin/bash

folder=$1
dir=$2

if [ ! -f "httrack2warc-0.2.1-shaded.jar" ]; then
    wget -O httrack2warc-0.2.1-shaded.jar https://github.com/nla/httrack2warc/releases/download/v0.2.1/httrack2warc-0.2.1-shaded.jar
fi

java -jar httrack2warc-0.2.1-shaded.jar "$dir/$folder"
