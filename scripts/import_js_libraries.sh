#!/bin/zsh

curl 'https://api.cdnjs.com/libraries?fields=filename,description,keywords,tutorials,alternativeNames,fileType,objectID,homepage,repository,author,license,version,github' | \
	jq '.results' | \
	sqlthemall -d 'postgresql://api:apipw@localhost:5432/storage' -t js_libraries
