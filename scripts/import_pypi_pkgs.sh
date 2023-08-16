#!/bin/zsh

cat requirements.txt requirements-dev.txt | \
	grep -o '^[^=]*' | \
	while read q; do
		curl -s "https://pypi.org/search/?q=${q}" | \
			grep -o '\/project\/[^\/]*' | \
	  		cut -c10- | \
	  		sed 's/\s*$//g' | \
	  		parallel "curl -s 'https://pypi.org/pypi/{}/json' | jq '.info' 2>/dev/null | sqlthemall -d 'postgresql://api:apipw@localhost:5432/storage' -t pypi_packages "
done

#for p in $(seq 1 100); do
#	echo 'curl -s --max-time 10 "https://pypi.org/search/?c=Topic+%3A%3A+Database&page='${p}'" | \
#	grep -o '\''\/project\/[^\/]*'\'' | \
#	cut -c10- ' | \
#	parallel -j 20 | \
#	sort --unique | \
#	shuf | \
#	parallel "curl -s --max-time 10 'https://pypi.org/pypi/{}/json' | jq '.info' 2>/dev/null | sqlthemall -d 'postgresql://api:apipw@localhost:5432/storage' -t pypi_packages "
#done 

