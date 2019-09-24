class Utils:
    maxLength = 16
    isHardCode = False
    sLenght = 0
    forced = False
    coeff=2
    parameters = ''

    def hcChar(self,n):
        if 'a' <= n <= 'z' or 'A' <= n <= 'Z' or '0' <= n <= '9' or n in self.parameters:
            return False
        else:
            return True

    def hardcoded(self, s):
        self.isHardCode = False
        for n in s:
            if not self.isHardCode and not self.hcChar(n):
                self.isHardCode = False
            else:
                self.isHardCode = True

    def escapeHc(self,hc):
        result = ''
        for i in hc:
            escape = ''
            if i in '.^$*+?{}[]\|()':
                result = result + '\\' + i
            else:
                result = result + i
        return result

    def filterAndRepetitions(self, currentFilter, filter, n, rep):
        if 'a' <= n <= 'z':
            currentFilter = 'a-z'
        elif 'A' <= n <= 'Z':
            currentFilter = 'A-Z'
        elif '0' <= n <= '9':
            currentFilter = '0-9'
        elif n in self.parameters:
            currentFilter = self.escapeHc(n)
        if filter == '':
            filter = currentFilter
        if filter == currentFilter:
            rep = rep + 1
        return currentFilter, filter, rep

    def checkSingleGroup(self, m, mandatory, regex, s, min, max):
        optionalCount = 0
        for m in s:
            optional = False

            if 's' in m and not 'optional' in m:
                filters = m['filters']
                for f in filters:
                    if 'optional' in f:
                        optionalCount = optionalCount + 1
                        optional = True
                    if not 'optional' in f:
                        mandatory = mandatory + 1

            if 'hc' not in m and 'optional' in m:
                optionalCount = optionalCount + 1
                optional = True
            #if not 'optional' in m and not optional:  # and not 'hc' in m:
            #    mandatory = mandatory + 1

        if self.forced == False and optionalCount > mandatory:
            if min >= 0:
                regex = '.' + '{' + str(min) + ',' + str(max) + '}'
            else:
                regex = '.' + '{' + str(max) + '}'
        return mandatory, optionalCount, regex

    def postRegex(self, i, mutual, optional, regex, s):
        if ((optional == True) or (mutual == True)) and i == len(s):
            regex = regex + ')?'
            open = False
        return regex

    def preRegex(self, i, m, mutual, optional, regex, s):
        if (mutual == True):
            regex = regex + ')'
            mutual = False
        if optional == True and (not 'optional' in m or 'hc' in m) and not i == len(s):
            regex = regex + ')?'
            optional = False
            #optionalCount = optionalCount + 1
        if optional == False and 'optional' in m:
            regex = regex + '('
            optional = True
            #optionalCount = optionalCount + 1
        if not 'optional' in m and not 'hc' in m:
            pass
            #mandatory = mandatory + 1
        if 'mutual' in m:  # and 'prefix' in m:
            regex = regex + '('
            mutual = True
        return mutual, optional, regex

    def repetitions(self, maxRepetitions2, minRepetitions2, repetitions1, repetitions2):
        r = 0
        minR = 0
        maxR = 0
        if (repetitions2 == 0):
            r = 0
            if repetitions1 < minRepetitions2:
                minR = repetitions1
            else:
                minR = minRepetitions2

            if repetitions1 > maxRepetitions2:
                maxR = repetitions1
            else:
                maxR = maxRepetitions2

        else:
            if repetitions1 == repetitions2:
                r = repetitions1
            elif repetitions1 < repetitions2:
                minR = repetitions1
                maxR = repetitions2
            else:
                minR = repetitions2
                maxR = repetitions1
        return maxR, minR, r

    def longestString(self, m1, m2):
        if len(m1['s']) > len(m2['s']):
            maxL = len(m1['s'])
            maxS = m1['s']
            minL = len(m2['s'])
            minS = m2['s']
        else:
            maxL = len(m2['s'])
            maxS = m2['s']
            minL = len(m1['s'])
            minS = m1['s']
        return maxS, maxL,minS,minL

    def longestMinDifference(self, struct1, struct2):
        if len(struct1) < len(struct2):
            minLength = len(struct1)
            lengthDifference = len(struct2) - minLength
            longest = struct2
        else:
            minLength = len(struct2)
            lengthDifference = len(struct1) - minLength
            longest = struct1
        return lengthDifference, minLength, longest

    def makeOptional(self, m):
        m['optional'] = True

    def makeMutual(self, m):
        m['mutual'] = True



