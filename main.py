import re
import utils
def regex(s):
    util = utils.Utils()
    util.maxLength = 20
    regexMap = util.singleGroupStructure(s)
    regex = util.regexString(regexMap)
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
#"""

"""
s1 = 'SBHLDB46L22H330P'
s2 = 'LKVVGL75M43C783A'
#"""

"""
s1 = 'SBHLDB46L22H330P'
s2 = 'LKVVGL75M43C783A'
#"""

#"""
s1 = '2857ef18-d549-11e9-bb65-2a2ae2dbcce4'
s2 = '2857f3f0-d549-11e9-bb65-2a2ae2dbcce4'
#"""

"""
s1 = 'aaa123'
s2 = 'aaa'
"""

print(s1)
regexMap1 = util.regexStructure(s1)
print(regexMap1)
regexString1 = util.regex(regexMap1)
print(regexString1)

print(s2)
regexMap2 = util.regexStructure(s2)
print(regexMap2)
regexString2 = util.regex(regexMap2)
print(regexString2)

merged = util.merge(regexMap1,regexMap2)
print('**************')
print(merged)

#regex1f = util.regexStringForced(regexMap1)
#regex2f = util.regexStringForced(regexMap2)
#print(regex1f)
#print(regex2f)



#p = re.compile('[a-z]{2}([a-z]{1})?[0-9]{3}')
#p = re.compile(fusion)
#p = re.compile(fusionf)
#m = p.match(s1)
#print(m)
#m = p.match(s2)
#print(m)


#regex("£££abc123_%&abc___")
#regex("123_abc")
#regex("123&abc")
#regex("1232_&_321")
#regex("328-02-90-136")
#regex("un due tre stella 56 7 999")
#print('***************************')
#print('abc123abc123')
#regex('abc123abc123')
#regexForced('abc123abc123')
#print('***************************')
#print('abc123abc')
##regex('abc123abc')
#regexForced('abc123abc')
#print('***************************')
#print('abc123')
#regex('abc123')
#regexForced('abc123')
#print('***************************')
#print('1616161616161616')
#regex('1616161616161616')
#print('***************************')
#print('17171717171717171')
#regex('17171717171717171')
#print('***************************')
#print('a22zz-c37-d11abc')
#regex('a22zz-c37-d11abc')
#regexForced('a22zz-c37-d11abc')

#print('***************************')
#print('a22zz-c37-d11')
##regex('a22zz-c37-d11')
#regexForced('a22zz-c37-d11')

#regex('abc')
#regex('123')

#[a-z]{3}
#[0-9]{3}
#p = re.compile('[a-z]{3}|[0-9]{3}')
#m = p.match('abc123')
#print(m)

















