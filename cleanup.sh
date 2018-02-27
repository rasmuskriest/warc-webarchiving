#!/bin/bash

if [[ $1 == "-f" ]];
then
    find -mindepth 1 -type f -iname '*.sqlite' -exec rm -f {} \;
    find -mindepth 1 -type f -iname '*.cdx' -exec rm -f {} \;
    find -mindepth 1 -type f -iname '*.log' -exec rm -f {} \;
    find -mindepth 1 -type f -iname '*.warc.gz' -exec rm -f {} \;
    find ./wget -mindepth 1 -type d -exec rm -rf {} \;
else
    find -mindepth 1 -type f -iname '*.sqlite' -exec rm -i {} \;
    find -mindepth 1 -type f -iname '*.cdx' -exec rm -i {} \;
    find -mindepth 1 -type f -iname '*.log' -exec rm -i {} \;
    find -mindepth 1 -type f -iname '*.warc.gz' -exec rm -i {} \;
    find ./wget -mindepth 1 -type d -exec rm -ri {} \;
fi
