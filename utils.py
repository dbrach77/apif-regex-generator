class Utils:
    maxLength = 16
    isHardCode = False
    sLenght = 0
    forced = False

    def hardcoded(self, s):
        self.isHardCode = False
        for n in s:
            if not self.isHardCode and ('a' <= n <= 'z' or 'A' <= n <= 'Z' or '0' <= n <= '9'):
                self.isHardCode = False
            else:
                self.isHardCode = True

    def regexStructure(self, s):
        temp = ''
        hc = ''
        filters = []
        self.hardcoded(s)
        ishc = self.isHardCode
        l=0
        if  ishc == True:
            for n in s:
                l = l + 1
                #se ho finito la stringa o è un carattere hc e hc è vuoto vuolte dire che devo appendere un gruppo filtro
                if l == len(s) or not('a' <= n <= 'z' or 'A' <= n <= 'Z' or '0' <= n <= '9') and hc == '':
                    self.endOfString(filters, hc, l, n, s, temp)
                    temp = ''
                    hc = n
                #se hc non è vuoto e ho ancora carattere hc allungo hc
                elif hc != '' and not('a' <= n <= 'z' or 'A' <= n <= 'Z' or '0' <= n <= '9'):
                    hc = hc + n
                #se hc non è vuoto e
                elif hc != '' and (l == len(s) or ('a' <= n <= 'z' or 'A' <= n <= 'Z' or '0' <= n <= '9')):
                    filters.append({'hc': self.escapeHc(hc)})
                    hc = ''
                    temp = temp + n
                else:
                    temp = temp + n
        else:
            filters.append(self.singleGroupStructure(s))

        return filters

    def endOfString(self, filters, hc, l, n, s, temp):
        # fine stringa e hc valorizzato allora devo inserire un gruppo hc prima dell'ultimo gruppo filtro
        if l == len(s) and hc != '':
            filters.append({'hc': self.escapeHc(hc)})
        # fine stringa e carattere alfanumerico allora accodo a temp l'ultimo carattere al gruppo filtro
        if l == len(s) and 'a' <= n <= 'z' or 'A' <= n <= 'Z' or '0' <= n <= '9':
            temp = temp + n
        # appendo il guppo filtro
        filters.append(self.singleGroupStructure(temp))
        # fine striga e carattere hc allora accodo l'ultimo gruppo hc dopo l'ultimo gruppo filtro
        if l == len(s) and not ('a' <= n <= 'z' or 'A' <= n <= 'Z' or '0' <= n <= '9'):
            filters.append({'hc': self.escapeHc(n)})

    def escapeHc(self,hc):
        result = ''
        for i in hc:
            escape = ''
            if i in '.^$*+?{}[]\|()':
                result = result + '\\' + i
            else:
                result = result + i
        return result

    def singleGroupStructure(self, s):
        filter = ''
        currentFilter = ''
        rep = 0
        l = 0
        filters = []

        for n in s:
            l = l + 1
            currentFilter, filter, rep = self.filterAndRepetitions(currentFilter, filter, n, rep)

            f = {'filter': filter, 'repetitions': rep, 'minR':0, 'maxR':0}
            if filter != currentFilter:
                filters.append(f)
                filter = currentFilter
                rep = 1

            f = {'filter': filter, 'repetitions': rep, 'minR':0, 'maxR':0}
            if l == len(s):
                filters.append(f)

        struct = {'s':s,'l':len(s),'filters':filters}
        return struct

    def filterAndRepetitions(self, currentFilter, filter, n, rep):
        if 'a' <= n <= 'z':
            currentFilter = 'a-z'
        elif 'A' <= n <= 'Z':
            currentFilter = 'A-Z'
        elif '0' <= n <= '9':
            currentFilter = '0-9'
        if filter == '':
            filter = currentFilter
        if filter == currentFilter:
            rep = rep + 1
        return currentFilter, filter, rep

    def regex(self, s):
        regex =''
        i = 0
        optional = False
        mutual = False
        optionalCount = 0
        mandatory = 0

        for m in s:
            i = i +1
            mandatory, mutual, optional, optionalCount, regex = self.preRegex(i, m, mandatory, mutual, optional,optionalCount, regex, s)
            regex = regex + self.singleGroupRegex(m,optional)
            regex = self.postRegex(i, mutual, optional, regex, s)

        for m in s:
            optional = False
            if 's' in m:
                filters = m['filters']
                for f in filters:
                    if 'optional' in f:
                        optionalCount = optionalCount + 1
                        optional = True
            if 'optional' in m:
                optionalCount = optionalCount + 1
                optional = True
            if not optional:# and not 'hc' in m:
                mandatory = mandatory+1




        if self.forced == False and optionalCount > mandatory:
            regex = '.*'

        return regex,mandatory,optionalCount

    def postRegex(self, i, mutual, optional, regex, s):
        if ((optional == True) or (mutual == True)) and i == len(s):
            regex = regex + ')?'
            open = False
        return regex

    def preRegex(self, i, m, mandatory, mutual, optional, optionalCount, regex, s):
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
        return mandatory, mutual, optional, optionalCount, regex

    #get the regex from the list of filters
    def singleGroupRegex(self, m, optional):
        regex = ''

        if 's' in m:
            s = m['s']
            sLenght =  m['l']
            filters = m['filters']
            if (sLenght > self.maxLength or (sLenght > 1 and len(filters) > sLenght/2)):
                regex = '.*'
            else :
                for f in filters:
                    regex = self.singleFilterRegex(f, optional, regex)

        if 'hc' in m:
            regex = regex + m['hc']

        return regex

    def singleFilterRegex(self, f, optional, regex):
        if f['minR'] > 0 and f['maxR'] > 0:
            tmpregex = '[' + f['filter'] + ']' + '{' + str(f['minR']) + ',' + str(f['maxR']) + '}'
        elif 1 < f['repetitions']:
            tmpregex = '[' + f['filter'] + ']' + '{' + str(f['repetitions']) + '}'
        else:
            tmpregex = '[' + f['filter'] + ']'
        # """
        if 'optional' in f and optional == False:
            tmpregex = '(' + tmpregex + ')?'
        # """
        regex = regex + tmpregex
        return regex

    def merge(self, struct1, struct2):
        minLength = 0
        filters = []
        merge = []
        lengthDifference, minLength, longestStruct = self.longestMinDifference(struct1, struct2)

        offset = 0
        for i in range(minLength):
            offset = offset + 1
            m1 = struct1[i]
            m2 = struct2[i]

            if 's' in m1:
                self.mergeFilters(filters, m1, m2, merge)

            if 'hc' in m1 and 'hc' in m2:
                filters = []
                self.mergeHc(m1, m2, merge)

        for minLength in range(lengthDifference):
            m = longestStruct[minLength+offset]
            if 's' in m:
                self.makeOptional(m)
                merge.append(m)
            if 'hc' in m:
                hardcode = {'hc': m['hc']}
                self.makeOptional(hardcode)
                merge.append(hardcode)

        return merge

    def mergeFilters(self, filters, m1, m2, merge):
        s, sl = self.longestString(m1, m2)
        filtersGroup1 = m1['filters']
        filtersGroup2 = m2['filters']
        lengthDifference, minLength, longestStruct = self.longestMinDifference(filtersGroup1, filtersGroup2)
        offset = 0

        for j in range(minLength):
            offset = self.mergeSingleGroup(filters, filtersGroup1, filtersGroup2, j, offset)

        for k in range(lengthDifference):
            group = longestStruct[k + offset]
            self.makeOptional(group)
            filters.append(group)

        struct = {'s': s, 'l': sl, 'filters': filters}

        if 'optional' in m2:
            self.makeOptional(struct)

        merge.append(struct)

    def mergeSingleGroup(self, filters, filtersGroup1, filtersGroup2, j, offset):
        filter1, filter2, group1, group2, maxRepetitions2, minRepetitions2, offset, repetitions1, repetitions2 = self.initSingleGroupMerge(filtersGroup1, filtersGroup2, j, offset)
        f = self.mergeFilter(filter1, filter2)
        maxR, minR, r = self.repetitions(maxRepetitions2, minRepetitions2, repetitions1, repetitions2)

        filter = {'filter': f, 'repetitions': r, 'minR': minR, 'maxR': maxR}

        if 'optional' in group1 or 'optional' in group2:
            self.makeOptional(filter)

        filters.append(filter)

        return offset



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

    def mergeFilter(self, filter1, filter2):
        if filter1 == filter2:
            f = filter1
        elif filter1 in filter2:
            f = filter2
        else:
            f = filter1 + filter2
        return f

    def initSingleGroupMerge(self, filtersGroup1, filtersGroup2, j, offset):
        offset = offset + 1
        group1 = filtersGroup1[j]
        group2 = filtersGroup2[j]
        filter1 = group1['filter']
        filter2 = group2['filter']
        repetitions1 = group1['repetitions']
        repetitions2 = group2['repetitions']
        minRepetitions2 = group2['minR']
        maxRepetitions2 = group2['maxR']
        return filter1, filter2, group1, group2, maxRepetitions2, minRepetitions2, offset, repetitions1, repetitions2

    def longestString(self, m1, m2):
        if len(m1['s']) > len(m2['s']):
            sl = len(m1['s'])
            s = m1['s']
        else:
            sl = len(m2['s'])
            s = m2['s']
        return s, sl

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

    def mergeHc(self, m1, m2, merge):
        hc1 = m1['hc']
        hc2 = m2['hc']
        if hc1 == hc2:
            hardcode = {'hc': hc1}
        elif hc1 in hc2:
            hardcode = {'hc': hc2}
            self.makeMutual(hardcode)
        elif hc2 in hc1:
            hardcode = {'hc': hc1}
            self.makeMutual(hardcode)
        else:
            hardcode = {'hc': m1['hc'] + '|' + m2['hc']}
            self.makeMutual(hardcode)

        if 'optional' in m2:
            self.makeOptional(hardcode)

        merge.append(hardcode)

    def makeOptional(self, m):
        m['optional'] = True

    def makeMutual(self, m):
        m['mutual'] = True



