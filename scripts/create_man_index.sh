#!/bin/zsh

# Autocompletion
for i in /usr/share/man/man1/* /usr/share/man/man8/*; do
	printf 'FT.SUGADD cmp_manpages "%s" 1\n' "${i:t:r:r}"
done | sort --unique | redis-cli

# Search Results
env_parallel --session

strip() {
        cat - | sed 's/^\s*//g' | sed 's/\s*$//g'
}

sql_escape() {
	sed -e 's/"/\\"/g' <<< "$@" | tr -d '\000'
}

# Create Index
( printf  'FT.CREATE manpages ON HASH PREFIX 1 manpages: SCHEMA  command TEXT WEIGHT 15.0 description TEXT WEIGHT 5.0 group TEXT WEIGHT 5.0 section TEXT WEIGHT 2.0 docpath TEXT WEIGHT 1.0 body TEXT WEIGHT 1.0\n' | redis-cli ) || printf 'Index manpages allready availible\n'

insertman() {
	body=$((MANWIDTH=1000 man --pager="/bin/cat" --local-file "${1}" 2>/dev/null ) || printf '')
	name=$(printf '%s\n' "${body}" | grep -A1 '^NAME' 2>/dev/null | sed '$!d')

        description=$(sql_escape $(printf '%s\n' "${name}" | sed 's/.*[—-] //'))
        section=$( sql_escape $( ( printf '%s\n' "${body}" | sed '1!d' | grep -o '([^)]*)'  | sed '1!d' | tr -d '()' | tr '[A-Z]' '[a-z]' ) || printf ''))
        replace=$( ( printf '%s\n' "${body}" | sed '1!d' | grep -o '^[^)]*)' ) || printf '  ')
        group=$( ( printf '%s\n' "${body}" | sed '1!d' | sed "s/${replace}//g" | strip ) || printf '')
        docpath=$(printf '%s' "${1}")
	Command=$(sql_escape $(printf '%s' "${1:t:r:r}"))
	body=$(sql_escape $(printf '%s' "${body}"))
	printf '%s\n' "${Command}"
	printf 'hset manpages:%s command "%s" description "%s" group "%s" section "%s" docpath "%s" body "%s"\n' "${2}" "${Command}" "${description}" "${group}" "${section}" "${docpath}" "${body}" | redis-cli #>/dev/null
}

n=1
for i in /usr/share/man/man1/* /usr/share/man/man8/*; do
#for i in /usr/share/man/man1/a* ; do
	n=$(printf '%s + 1\n' "${n}" | bc)
	printf 'insertman "%s" "%s"\n' "${i}" "${n}"
done | env_parallel -j 30 
