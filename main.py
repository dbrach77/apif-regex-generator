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
    print(lineList[i])
    inputMap = util.regexStructure(lineList[i])
    #print(util.regex(inputMap))
    if i == 0:
        mergeMap = inputMap
    else:
        mergeMap = util.merge(inputMap, mergeMap)

print('MERGE')
print(mergeMap)
regex = util.regex(mergeMap)
print(regex)


print('************** Matches')
for i in range(len(lineList)):
    p = re.compile(regex)
    print(p.match(lineList[i]))





















