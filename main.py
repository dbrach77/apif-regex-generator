import re
import utils
def regex(s,forced):
    util = utils.Utils()
    util.maxLength = 16
    regexMap = util.regexMap(s)
    regex = util.regexString(regexMap,forced)
    p = re.compile(regex)
    m = p.findall(s)
    #print(m)
    print(regex)


#regex("£££abc123_%&abc___")
#regex("123_abc")
#regex("123&abc")
#regex("1232_&_321")
#regex("328-02-90-136")
#regex("un due tre stella 56 7 999")
print('***************************')
print('abc123abc123')
regex('abc123abc123',False)
regex('abc123abc123',True)
print('***************************')
print('abc123abc')
regex('abc123abc',False)
regex('abc123abc',True)
print('***************************')
print('abc123')
regex('abc123',False)
regex('abc123',True)
print('***************************')
print('1616161616161616')
regex('1616161616161616',False)
print('***************************')
print('17171717171717171')
regex('17171717171717171',False)
print('***************************')
print('a22zz-c37-d11abc')
regex('a22zz-c37-d11abc',False)
regex('a22zz-c37-d11abc',True)

print('***************************')
print('a22zz-c37-d11')
regex('a22zz-c37-d11',False)
regex('a22zz-c37-d11',True)

regex('abc',False)
regex('123',False)

#[a-z]{3}
#[0-9]{3}
p = re.compile('[a-z]{3}|[0-9]{3}')
m = p.match('abc123')
print(m)

















