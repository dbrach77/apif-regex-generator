import re
import utils
def regex(s):
    util = utils.Utils()
    regexMap = util.regexMap(s)
    regex = util.regexString(regexMap)
    p = re.compile(regex)
    m = p.findall(s)
    print(m)
    print(regex)


regex("£££abc123_%&abc___")
regex("123_abc")
regex("123&abc")
regex("1232_&_321")
regex("328-02-90-136")
regex("un due tre stella 56 7 999")
















