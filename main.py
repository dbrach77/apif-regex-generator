import re
import sys

import utils
def regex(s):
    util = utils.Utils()
    util.maxLength = 20
    regexMap = util.singleGroupStructure(s)
    regex = util.singleGroupRegex(regexMap)
    p = re.compile(regex)
    m = p.findall(s)
    #print(m)
    print(regex)

def regexForced(s):
    util = utils.Utils()
    util.maxLength = 40
    regexMap = util.singleGroupStructure(s)
    regex = util.regexStringForced(regexMap)
    p = re.compile(regex)
    m = p.findall(s)
    #print(m)
    print(regex)

def test():
    util = utils.Utils()
    util.maxLength = 36

    #p = re.compile(regexString2)
    #m = p.match(s2)
    #print(m)

    #ora per il cazzo id merge. avendo una struttura figa, nel caso di hard code posso recuperare per ogni elemento la sua stringa e gestire il .* OLE!!!
    #prima va fatto un controllo su dimennsione della struttra. se hanno dimensioni simili ok.
    #se harccoded posso guardare la dimensione dei singoi pezzi. e se hanno le stesse hc. in pratica devono essere simili posizione per posizione


    """
    s1 = '1.1.1.1'
    s2 = '111.111.111.111'
    s3 = '11.1.11.11'
    s4 = '111.111.111.1'
    #"""

    """
    s1 = 'SBHLDB46L22H330R'
    s2 = 'LKVVGL75M43C783A'
    s3 = 'LKVVGL75M43C781G'
    #"""

    """
    s1 = '2857ef18-d549-11e9-bb65-2a2ae2dbcce4'
    s2 = '2857f3f0-d549-11e9-bb65-2a2ae2dbcce4'
    s3 = '2857f3f0-d549-1111-bb65-2a2ae2dbcce4'
    #"""

    """
    s1 = '5d7b5e00f894261071b552d0'
    s2 = '5d7b5e1a214a01a47eb26c5c'
    s3 = '5d7b5e1a214a01a47eb26c5c'
    #"""

    """
    s1 = '014-76-3875'
    s2 = '204-72-7894'
    #"""

    """
    s1 = 'abcd_1234'
    s2 = '1234'
    #"""

    """
    s1 = '014-7676-3875'
    s2 = '204-72-7894'
    #"""

    #"""
    s1 = '014-7a7a-3875'
    s2 = '204-77aa77bb-7894'
    s3 = '014-7a7a-3875'
    #"""

    """
    s1 = 'a1a1a1a1a1'
    s2 = 'b2b2b2b2b2'
    s3 = 'aaa_1234'
    s4 = 'aaa_1234'
    #"""

    print('************** s1')
    print(s1)
    regexMap1 = util.regexStructure(s1)
    print(regexMap1)
    regexString1 = util.regex(regexMap1)
    print(regexString1)

    print('************** s2')
    print(s2)
    regexMap2 = util.regexStructure(s2)
    print(regexMap2)
    regexString2 = util.regex(regexMap2)
    print(regexString2)

    merged = util.merge(regexMap1, regexMap2)
    print(merged)
    print(util.regex(merged))


    print('************** s3')
    print(s3)
    regexMap3 = util.regexStructure(s3)
    print(regexMap3)
    regexString3 = util.regex(regexMap3)
    print(regexString3)

    merged = util.merge(regexMap3, merged)
    print(merged)
    print(util.regex(merged))

    """
    print('************** Matches')
    p = re.compile(merged)
    print(p.match(s1))
    print(p.match(s2))
    """


#test()
util = utils.Utils()
util.maxLength = 36
print(sys.argv[1])
fileName = sys.argv[1]
lineList = [line.rstrip('\n') for line in open(fileName)]

for i in range(len(lineList)):
    #print('INPUT')
    print(lineList[i])
    inputMap = util.regexStructure(lineList[i])
    #print(inputMap)
    print(util.regex(inputMap))
    if i == 0:
        mergeMap = inputMap
    else:
        print('MERGE')
        mergeMap = util.merge(inputMap, mergeMap)
        #print(mergeMap)
        print(util.regex(mergeMap))



















