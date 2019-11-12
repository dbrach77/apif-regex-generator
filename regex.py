class Regex:

    import utils

    util = utils.Utils()
    maxLength = 36
    parameters = ''

    def regexStructure(self, source):
            filter = ''
            hc = ''
            filters = []
            self.util.hardcoded(source)
            ishc = self.util.isHardCode
            index=0
            if  ishc == True:
                for c in source:
                    index = index + 1
                    #se ho finito la stringa o è un carattere hc e hc è vuoto vuolte dire che devo appendere un gruppo filtro
                    if index == len(source) or self.util.hcChar(c) and hc == '':
                        self.endOfString(filters, hc, index, c, source, filter)
                        filter = ''
                        hc = c
                    #se hc non è vuoto e ho ancora carattere hc allungo hc
                    elif hc != '' and self.util.hcChar(c):
                        hc = hc + c
                    #se hc non è vuoto e
                    elif hc != '' and (index == len(source) or not self.util.hcChar(c)):
                        filters.append({'hc': self.util.escapeHc(hc)})
                        hc = ''
                        filter = filter + c
                    else:
                        filter = filter + c
            else:
                filters.append(self.singleGroupStructure(source))

            #aggiungo la lunghezza minima e massima delle stringhe in esame
            filters.append({'sourceMin':len(source)})
            filters.append({'sourceMax':len(source)})
            return filters

    def endOfString(self, filters, hc, index, c, source, filter):
        # fine stringa e hc valorizzato allora devo inserire un gruppo hc prima dell'ultimo gruppo filtro
        if index == len(source) and hc != '':
            filters.append({'hc': self.util.escapeHc(hc)})
        # fine stringa e carattere alfanumerico allora accodo a temp l'ultimo carattere al gruppo filtro
        if index == len(source) and not self.util.hcChar(c):
            filter = filter + c
        # appendo il guppo filtro
        filters.append(self.singleGroupStructure(filter))
        # fine striga e carattere hc allora accodo l'ultimo gruppo hc dopo l'ultimo gruppo filtro
        if index == len(source) and self.util.hcChar(c):
            filters.append({'hc': self.util.escapeHc(c)})


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
        mandatory = 0
        min = 0
        max = 0

        for m in s:
           if ('sourceMin' in m): min = m['sourceMin']
           if ('sourceMax' in m): max = m['sourceMax']

        for m in s:
            i = i +1
            temp,tmpmin,tmpmax = self.singleGroupRegex(m,optional,min,max)
            regex = regex + temp

        mandatory, optionalCount, regex = self.util.checkSingleGroup(m, mandatory, regex, s, min, max)
        return regex,mandatory,optionalCount

    #get the regex from the list of filters
    def singleGroupRegex(self, m, optional,min,max):
        regex = ''

        if 's' in m:
            s = m['s']
            sLenght =  m['l']
            filters = m['filters']
            for f in filters:
                regex,tmpmin,tmpmax = self.singleFilterRegex(f, optional, regex)

            if 'optional' in m:
                regex = '(' + regex + ')?'

            if ('sourceMin' in m): min = m['sourceMin']
            if ('sourceMax' in m): max = m['sourceMax']

            if (sLenght > self.maxLength or (sLenght > 1 and len(filters) > sLenght/2)):
                if (min == max):
                    regex = '.'+'{'+str(max)+'}'
                else:
                    regex = '.'+'{'+str(min)+','+str(max)+'}'

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

        regex = regex + tmpregex
        return regex,min,max

    def merge(self, struct1, struct2):
        sourceMin1 = 0
        sourceMax1 = 0
        sourceMin2 = 0
        sourceMax2 = 0
        filters = []
        merge = []

        #max and min from structure 1
        for m in struct1:
            if ('sourceMin' in m): sourceMin1 = m['sourceMin']
            if ('sourceMax' in m): sourceMax1 = m['sourceMax']
        #max and min from structure 2
        for m in struct2:
            if ('sourceMin' in m): sourceMin2 = m['sourceMin']
            if ('sourceMax' in m): sourceMax2 = m['sourceMax']
        #cleaning structure 1 form navigation purposes
        for m in struct1:
            if ('sourceMin' in m): struct1.remove(m)
        for m in struct1:
            if ('sourceMax' in m): struct1.remove(m)
        #cleaning structure 2 form navigation purposes
        for m in struct2:
            if ('sourceMin' in m): struct2.remove(m)
        for m in struct2:
            if ('sourceMax' in m): struct2.remove(m)

        if (sourceMin1 < sourceMin2):
            sourceMin = sourceMin1
        else:
            sourceMin = sourceMin2

        if (sourceMax1 > sourceMax2):
            sourceMax = sourceMax1
        else:
            sourceMax = sourceMax2

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

        merge.append({'sourceMin':sourceMin})
        merge.append({'sourceMax':sourceMax})
        return merge

    #filters merge
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

    #mergin single group
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
        elif hc1 in hc2 and '|' in hc2:
            hardcode = {'hc': hc2}
            self.util.makeMutual(hardcode)
        elif hc2 in hc1 and '|' in hc1:
            hardcode = {'hc': hc1}
            self.util.makeMutual(hardcode)
        else:
            hardcode = {'hc': m1['hc'] + '|' + m2['hc']}
            self.util.makeMutual(hardcode)

        if 'optional' in m2:
            self.util.makeOptional(hardcode)

        merge.append(hardcode)
