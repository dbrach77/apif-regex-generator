import re
import sys

import utils
import regex


rgx = regex.Regex()
rgx.maxLength = 36
print(sys.argv[1])
fileName = sys.argv[1]
lineList = [line.rstrip('\n') for line in open(fileName)]

print('INPUT')
for i in range(len(lineList)):
    #print(lineList[i])
    inputMap = rgx.regexStructure(lineList[i])
    #print(inputMap)
    #print(util.regex(inputMap))
    if i == 0:
        mergeMap = inputMap
    else:
        mergeMap = rgx.merge(inputMap, mergeMap)
    #print(mergeMap)

print('MERGE')
print(mergeMap)
regex,mandatory,optional = rgx.regex(mergeMap)
print(str(mandatory))
print(str(optional))

#regex = '.{0,43}'
print(regex)
regex = '^'+regex+'$'
matches = 0
print('************** Matches')
for i in range(len(lineList)):
    p = re.compile(regex)
    match = p.match(lineList[i])
    if (match != None and match.string == lineList[i]):
        matches = matches + 1
        print(match)

if matches == len(lineList):
    print('************** ALL Matches')
else:
    print('************** NOT Matches')
    for i in range(len(lineList)):
        p = re.compile(regex)
        match = p.match(lineList[i])
        if match == None or match.string != lineList[i]:
            print(lineList[i])


rgx.util.forced = True
regex,mandatory,optional = rgx.regex(mergeMap)
print(regex)























