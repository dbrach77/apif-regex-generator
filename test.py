import re
regex = '^[0-9.(][0-9-]{1,11}[0-9.)]$'
print(regex)
s='(91999999999)'
p = re.compile(regex)
match = p.match(s)
print(match)
s='1-8379999999'
print(regex)
p = re.compile(regex)
match = p.match(s)
print(match)
