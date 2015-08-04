#!/bin/bash

array=( "https://github.com" "https://status.github.com/" "https://developer.github.com/" )

for i in "${array[@]}"
do
	python crawler.py -d 0 -u -p "/var/tmp/downloaded/" "$i"
done
