import re
import sys

import utils
import regex


rgx = regex.Regex()
rgx.maxLength = 36
fileName = sys.argv[1]
print(sys.argv[1])
if (len(sys.argv) == 3):
    rgx.util.parameters = sys.argv[2]
    print(sys.argv[2])
#rgx.util.parameters = ''

lineList = [line.rstrip('\n') for line in open(fileName)]

#print('INPUT')
for i in range(len(lineList)):
    #print(lineList[i])
    inputMap = rgx.regexStructure(lineList[i])
    #print(inputMap)
    #print(util.regex(inputMap))
    if i == 0:
        mergeMap = inputMap
    else:
        mergeMap = rgx.merge(inputMap, mergeMap)
print(mergeMap)

def matchRegex():
    global regex, mandatory, optional, i
    print('MERGE NO EURISTICS')
    rgx.util.forced = True
    #print(mergeMap)
    regex, mandatory, optional = rgx.regex(mergeMap)
    print(str(mandatory))
    print(str(optional))
    #regex = '[0-9]{3}(-|\.)[0-9]{3}(-|\.)[0-9]{4}( )?([a-z][0-9]{3})?'
    print(regex)
    regex = '^' + regex + '$'
    matches = 0
    # print('************** Matches')
    for i in range(len(lineList)):
        p = re.compile(regex)
        match = p.match(lineList[i])
        if (match != None and match.string == lineList[i]):
            matches = matches + 1
            # print(match)
    if matches == len(lineList):
        print('************** ALL Matches')
    else:
        print('************** NOT Matches')
        for i in range(len(lineList)):
            p = re.compile(regex)
            match = p.match(lineList[i])
            if match == None or match.string != lineList[i]:
                print(lineList[i])


def matchEuristicRegex():
    global regex, mandatory, optional, i
    print('MERGE WITH EURISTICS')
    rgx.util.forced = False
    # print(mergeMap)
    regex, mandatory, optional = rgx.regex(mergeMap)
    print(str(mandatory))
    print(str(optional))
    # regex = '[a-z]{11}[.][0-9]{3}'
    print(regex)
    regex = '^' + regex + '$'
    matches = 0
    # print('************** Matches')
    for i in range(len(lineList)):
        p = re.compile(regex)
        match = p.match(lineList[i])
        if (match != None and match.string == lineList[i]):
            matches = matches + 1
            # print(match)
    if matches == len(lineList):
        print('************** ALL Matches')
    else:
        print('************** NOT Matches')
        for i in range(len(lineList)):
            p = re.compile(regex)
            match = p.match(lineList[i])
            if match == None or match.string != lineList[i]:
                print(lineList[i])


matchRegex()
matchEuristicRegex()


























