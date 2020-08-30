#!/bin/bash
# history -w /dev/stdout
# -> will write the history to stddev (used in contrast to a plain "history" command to cut of the line numbers)
#
# grep '\<sudo\>[[:space:]+][a-z]'
# -> searches the output of the previous command for the word 'sudo' followed by one or more whitespaces/tabs and
# at least one letter (I assume all commands start with a letter and no one made an alias starting with a number).
# This will ensure that we also match piped sudo commands like:
# echo 'something' |sudo ls
# If we assume sudo will always be used as first command we can use:
# grep -w '^sudo'
#
# sed -r 's/\s+/ /g'
# -> reduce all whitespaces to a single blank in case someone made a typo
#
# sed -r 's/\s+$//g'
# -> delete trailing whitespaces
#
# sort
# -> sorts the remaining commands in the history so uniq can count them correctly
#
# uniq -c
# -> merges the now sorted lines to the first occurence and counts the occurences

 history -w /dev/stdout | grep '\<sudo\>[[:space:]+][a-z]' | sed -r 's/\s+/ /g' | sed -r 's/\s+$//g' | sort | uniq -c