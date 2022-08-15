#!/bin/zsh

curl 'https://api.cdnjs.com/libraries?fields=filename,description,keywords,tutorials,alternativeNames,fileType,objectID,homepage,repository,author,license,version,github' | \
	jq '.results' | \
	sqlthemall -d 'postgresql://crawler:crawler@localhost:5432/crawler' -t js_libraries
