class Regex:

    import utils

    util = utils.Utils()
    maxLength = 36
    parameters = ''

    def regexStructure(self, s):
            temp = ''
            hc = ''
            filters = []
            self.util.hardcoded(s)
            ishc = self.util.isHardCode
            l=0
            if  ishc == True:
                for n in s:
                    l = l + 1
                    #se ho finito la stringa o è un carattere hc e hc è vuoto vuolte dire che devo appendere un gruppo filtro
                    if l == len(s) or self.util.hcChar(n) and hc == '':
                        self.endOfString(filters, hc, l, n, s, temp)
                        temp = ''
                        hc = n
                    #se hc non è vuoto e ho ancora carattere hc allungo hc
                    elif hc != '' and self.util.hcChar(n):
                        hc = hc + n
                    #se hc non è vuoto e
                    elif hc != '' and (l == len(s) or not self.util.hcChar(n)):
                        filters.append({'hc': self.util.escapeHc(hc)})
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
            filters.append({'hc': self.util.escapeHc(hc)})
        # fine stringa e carattere alfanumerico allora accodo a temp l'ultimo carattere al gruppo filtro
        if l == len(s) and not self.util.hcChar(n):
            temp = temp + n
        # appendo il guppo filtro
        filters.append(self.singleGroupStructure(temp))
        # fine striga e carattere hc allora accodo l'ultimo gruppo hc dopo l'ultimo gruppo filtro
        if l == len(s) and self.util.hcChar(n):
            filters.append({'hc': self.util.escapeHc(n)})

    def singleGroupStructure(self, s):
        filter = ''
        currentFilter = ''
        rep = 0
        l = 0
        filters = []

        for n in s:
            l = l + 1
            currentFilter, filter, rep = self.util.filterAndRepetitions(currentFilter, filter, n, rep)

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

    def regex(self, s):
        regex =''
        i = 0
        optional = False
        mutual = False
        hardcoded = False
        optionalCount = 0
        mandatory = 0
        min = 0
        max = 0

        for m in s:
            i = i +1
            #mutual, optional, regex = self.util.preRegex(i, m, mutual, optional, regex, s)
            temp,tmpmin,tmpmax = self.singleGroupRegex(m,optional)
            regex = regex + temp
            #regex = self.util.postRegex(i, mutual, optional, regex, s)
            #if min == 0 or tmpmin < min:
            min = tmpmin
            max = max + tmpmax

        for m in s:
            if 's' in m:
                filters = m['filters']
                for f in filters:
                    if 'hc' in f:
                        hardcoded = True
            if 'hc' in m:
                hardcoded = True
        optionalCount = 0
        mandatory, optionalCount, regex = self.util.checkSingleGroup(m, mandatory, regex, s, min, max)
        return regex,mandatory,optionalCount

    #get the regex from the list of filters
    def singleGroupRegex(self, m, optional):
        regex = ''
        min = 0
        max = 0

        if 's' in m:
            s = m['s']
            sLenght =  m['l']
            filters = m['filters']
            for f in filters:
                regex,tmpmin,tmpmax = self.singleFilterRegex(f, optional, regex)
                if min == 0 or tmpmin < min:
                    min = tmpmin
                max = max + tmpmax

            if 'optional' in m:
                regex = '(' + regex + ')?'

            if (sLenght > self.maxLength or (sLenght > 1 and len(filters) > sLenght/2)):
                if 'minL' in m:
                    regex = '.'+'{'+str(min)+','+str(sLenght)+'}'
                else:
                    regex = '.'+'{'+str(sLenght)+'}'

        if 'hc' in m:
            if 'optional' in m:
                regex = regex + '('+m['hc']+')?'
            elif 'mutual' in m:
                regex = regex + '('+m['hc']+')'
            else:
                regex = regex + m['hc']
            max = len(m['hc'])


        return regex,min,max

    def singleFilterRegex(self, f, optional, regex):
        if f['minR'] > 0 and f['maxR'] > 0:
            tmpregex = '[' + f['filter'] + ']' + '{' + str(f['minR']) + ',' + str(f['maxR']) + '}'
            min = f['minR']
            max = f['maxR']
        elif 1 < f['repetitions']:
            tmpregex = '[' + f['filter'] + ']' + '{' + str(f['repetitions']) + '}'
            min = 0
            max = f['repetitions']
        else:
            tmpregex = '[' + f['filter'] + ']'
            min = 0
            max = 1

        if 'optional' in f:
            max = f['repetitions']

        if 'optional' in f:
            tmpregex = '(' + tmpregex  + ')?'
            #optional = True
        """
        if 'optional' in f and optional == False:
            tmpregex = '(' + tmpregex # + ')?'
            optional = True
        if not 'optional' in f and optional == True:
            #tmpregex = ')?' + tmpregex # +
            optional = False

        # """

        regex = regex + tmpregex
        return regex,min,max

    def merge(self, struct1, struct2):
        minLength = 0
        filters = []
        merge = []
        lengthDifference, minLength, longestStruct = self.util.longestMinDifference(struct1, struct2)

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
                self.util.makeOptional(m)
                merge.append(m)
            if 'hc' in m:
                hardcode = {'hc': m['hc']}
                self.util.makeOptional(hardcode)
                merge.append(hardcode)

        return merge

    def mergeFilters(self, filters, m1, m2, merge):
        maxS, maxL, minS, minL = self.util.longestString(m1, m2)
        filtersGroup1 = m1['filters']
        filtersGroup2 = m2['filters']
        lengthDifference, minLength, longestStruct = self.util.longestMinDifference(filtersGroup1, filtersGroup2)
        offset = 0

        for j in range(minLength):
            offset = self.mergeSingleGroup(filters, filtersGroup1, filtersGroup2, j, offset)

        for k in range(lengthDifference):
            group = longestStruct[k + offset]
            self.util.makeOptional(group)
            filters.append(group)

        struct = {'s': maxS, 'l': maxL, 'minS':minS, 'minL':minL, 'filters': filters}

        if 'optional' in m2:
            self.util.makeOptional(struct)

        merge.append(struct)

    def mergeSingleGroup(self, filters, filtersGroup1, filtersGroup2, j, offset):
        filter1, filter2, group1, group2, maxRepetitions2, minRepetitions2, offset, repetitions1, repetitions2 = self.initSingleGroupMerge(filtersGroup1, filtersGroup2, j, offset)
        f = self.mergeFilter(filter1, filter2)
        maxR, minR, r = self.util.repetitions(maxRepetitions2, minRepetitions2, repetitions1, repetitions2)

        filter = {'filter': f, 'repetitions': r, 'minR': minR, 'maxR': maxR}

        if 'optional' in group1 or 'optional' in group2:
            self.util.makeOptional(filter)

        filters.append(filter)

        return offset

    def basicFilter(self,filter):
        if filter == 'a-z':
            return True
        if filter == 'A-A':
            return True
        if filter == '0-9':
            return True
        return False

    def mergeFilter(self, filter1, filter2):
        if filter1 == filter2:
            f = filter1
        elif filter1 in filter2 and not self.basicFilter(filter2):
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

    def mergeHc(self, m1, m2, merge):
        hc1 = m1['hc']
        hc2 = m2['hc']
        if hc1 == hc2:
            hardcode = {'hc': hc1}
        elif hc1 in hc2:
            hardcode = {'hc': hc2}
            self.util.makeMutual(hardcode)
        elif hc2 in hc1:
            hardcode = {'hc': hc1}
            self.util.makeMutual(hardcode)
        else:
            hardcode = {'hc': m1['hc'] + '|' + m2['hc']}
            self.util.makeMutual(hardcode)

        if 'optional' in m2:
            self.util.makeOptional(hardcode)

        merge.append(hardcode)
