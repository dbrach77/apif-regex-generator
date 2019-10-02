import re
import sys

import utils
import regex


rgx = regex.Regex()
rgx.maxLength = 36
fileName = sys.argv[1]
#print(sys.argv[1])
if (len(sys.argv) == 3):
    rgx.util.parameters = sys.argv[2]
    #print(sys.argv[2])
#rgx.util.parameters = ''

lineList = [line.rstrip('\n') for line in open(fileName)]

#print('INPUT')
for i in range(len(lineList)):
    inputMap = rgx.regexStructure(lineList[i])
    if i == 0:
        mergeMap = inputMap
    else:
        mergeMap = rgx.merge(inputMap, mergeMap)


def matchRegex():
    global regex, mandatory, optional, i
    rgx.util.forced = True
    regex, mandatory, optional = rgx.regex(mergeMap)
    #regex = '[a-z]{5,6}([\.][a-z]{5,7})?@[a-z]{5,11}[\.][a-z]{2,3}'
    print("True expression: "+ regex)
    regex = '^' + regex + '$'
    matches = 0
    for i in range(len(lineList)):
        p = re.compile(regex)
        match = p.match(lineList[i])
        if (match != None and match.string == lineList[i]):
            matches = matches + 1

    if matches == len(lineList):
        pass #print('************** ALL Matches')
    else:
        print('************** NOT Matches')
        for i in range(len(lineList)):
            p = re.compile(regex)
            match = p.match(lineList[i])
            if match == None or match.string != lineList[i]:
                print(lineList[i])


def matchEuristicRegex():
    global regex, mandatory, optional, i
    rgx.util.forced = False
    #print(mergeMap)
    regex, mandatory, optional = rgx.regex(mergeMap)
    print("Mandatory Groups: "+str(mandatory))
    print("Optionl Groups: "+str(optional))
    #regex = '[A-Z][a-z]{3,10}(, | )[A-Z][a-z]{4,8}(, | )?([A-Z][a-z]{7,12})?'
    print("Final expression: " + regex)
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
        pass #print('************** ALL Matches')
    else:
        print('************** NOT Matches')
        for i in range(len(lineList)):
            p = re.compile(regex)
            match = p.match(lineList[i])
            if match == None or match.string != lineList[i]:
                print(lineList[i])


#matchRegex()
matchEuristicRegex()


























