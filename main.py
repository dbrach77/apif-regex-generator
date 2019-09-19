import re
import sys

import utils


util = utils.Utils()
util.maxLength = 36
print(sys.argv[1])
fileName = sys.argv[1]
lineList = [line.rstrip('\n') for line in open(fileName)]

print('INPUT')
for i in range(len(lineList)):
    #print(lineList[i])
    inputMap = util.regexStructure(lineList[i])
    #print(inputMap)
    #print(util.regex(inputMap))
    if i == 0:
        mergeMap = inputMap
    else:
        mergeMap = util.merge(inputMap, mergeMap)

print('MERGE')
print(mergeMap)
regex,mandatory,optional = util.regex(mergeMap)
print(str(mandatory))
print(str(optional))
print(regex)

#regex = '([0-9]{1})?(\(|-|\.)[0-9]{3}(\) |-|\.)[0-9]{3,4}((-| )[0-9a-z]{1,4}[0-9]{3,5})?( [a-z][0-9]{3,5})?'
matches = 0
print('************** Matches')
for i in range(len(lineList)):
    p = re.compile(regex)
    match = p.match(lineList[i])
    if (match != None and match.string == lineList[i]):
        matches = matches + 1
        print(lineList[i])

if matches == len(lineList):
    print('************** ALL Matches')
else:
    print('************** NOT Matches')
    for i in range(len(lineList)):
        p = re.compile(regex)
        match = p.match(lineList[i])
        if match == None or match.string != lineList[i]:
            print(lineList[i])
























