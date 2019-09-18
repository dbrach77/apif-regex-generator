class Utils:
    maxLength = 16
    isHardCode = False
    sLenght = 0

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
                if l == len(s) or not('a' <= n <= 'z' or 'A' <= n <= 'Z' or '0' <= n <= '9') and hc == '':
                    if l == len(s) and hc != '':
                        filters.append({'hc': hc})
                    if l == len(s) and 'a' <= n <= 'z' or 'A' <= n <= 'Z' or '0' <= n <= '9':
                        temp = temp + n
                    filters.append(self.singleGroupStructure(temp))
                    temp = ''
                    hc = n
                elif hc != '' and not('a' <= n <= 'z' or 'A' <= n <= 'Z' or '0' <= n <= '9'):
                    hc = hc + n
                elif hc != '' and (l == len(s) or ('a' <= n <= 'z' or 'A' <= n <= 'Z' or '0' <= n <= '9')):
                    filters.append({'hc': hc})
                    hc = ''
                    temp = temp + n
                else:
                    temp = temp + n
        else:
            filters.append(self.singleGroupStructure(s))

        return filters

    def singleGroupStructure(self, s):
        filter = ''
        currentFilter = ''
        rep = 0
        l = 0
        filters = []

        for n in s:
            l = l + 1
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

            f = {'filter': filter, 'repetitions': rep, 'minR':0, 'maxR':0}
            if filter != currentFilter:
                filters.append(f)
                filter = currentFilter
                rep = 1

            f = {'filter': filter, 'repetitions': rep, 'minR':0, 'maxR':0}
            if l == len(s):
                filters.append(f)

        #self.sLenght = len(s)
        struct = {'s':s,'l':len(s),'filters':filters}
        return struct
        #return filters


    def regex(self, s):
        regex =''
        i = 0
        open = False
        closed = False

        for m in s:
            i = i +1

            if open == True and (not 'optional' in m or 'hc' in m) and not i == len(s):
                regex = regex + m['postfix']
                open = False

            if 'optional' in m and not open:
                regex = regex + m['prefix']
                open = True

            if 'mutual' in m and 'prefix' in m:
                regex = regex + m['prefix']

            regex = regex + self.singleGroupRegex(m)


            if 'mutual' in m and 'postfix' in m:
                regex = regex + m['postfix']

            if open == True and i == len(s):
                regex = regex + m['postfix']
                open = False


        return regex

    #get the regex from the list of filters
    def singleGroupRegex(self, m):
        regex = ''

        if 's' in m:
            s = m['s']
            sLenght =  m['l']
            filters = m['filters']
            if (sLenght > self.maxLength or (sLenght > 1 and len(filters) > sLenght/2)):
                regex = '.*'
            else :
                for f in filters:
                    if f['minR'] > 0 and f['maxR']>0:
                        tmpregex = '[' + f['filter'] +']' +'{' + str(f['minR']) +','+str(f['maxR'])+ '}'
                    elif 1 < f['repetitions']:
                        tmpregex = '[' + f['filter'] +']' +'{' + str(f['repetitions']) + '}'
                    else:
                        tmpregex = '[' + f['filter'] +']'

                    if 'optional' in f:
                        tmpregex = '('+tmpregex+')?'

                    regex = regex + tmpregex

        if 'hc' in m:
            regex = regex + m['hc']

        return regex

    def merge(self, struct1, struct2):
        l = 0
        filters = []
        merge = []
        if len(struct1) < len(struct2):
            l = len(struct1)
            diffFilters = len(struct2) - l
            longest = struct2
        else:
            l = len(struct2)
            diffFilters = len(struct1) - l
            longest = struct1

        offset = 0
        for i in range(l):
            offset = offset + 1
            m1 = struct1[i]
            m2 = struct2[i]

            if 's' in m1:
                self.mergeFilters(filters, m1, m2, merge)

            if 'hc' in m1 and 'hc' in m2:
                filters = []
                hc1 = m1['hc']
                hc2 = m2['hc']

                if hc1 == hc2:
                    hardcode = {'hc': hc1}
                    if 'optional' in m2:
                        hardcode['optional'] = True
                        hardcode['prefix'] = '('
                        hardcode['postfix'] = ')?'
                    merge.append(hardcode)
                elif hc1 in hc2:
                    hardcode = {'hc': hc2}
                    hardcode['mutual'] = True
                    hardcode['prefix'] = '['
                    hardcode['postfix'] = ']'
                    merge.append(hardcode)
                elif hc2 in hc1:
                    hardcode = {'hc': hc1}
                    hardcode['mutual'] = True
                    hardcode['prefix'] = '['
                    hardcode['postfix'] = ']'
                    merge.append(hardcode)
                else:
                    hardcode = {'hc': m1['hc']+'|'+m2['hc']}
                    hardcode['mutual'] = True
                    hardcode['prefix'] = '['
                    hardcode['postfix'] = ']'
                    merge.append(hardcode)

        for l in range(diffFilters):
            m = longest[l+offset]
            if 's' in m:
                m['optional'] = True
                m['prefix'] = '('
                m['postfix'] = ')?'
                merge.append(m)
            if 'hc' in m:
                hardcode = {'hc': m['hc']}
                hardcode['optional'] = True
                hardcode['prefix'] = '('
                hardcode['postfix'] = ')?'
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
            group['optional'] = True
            group['prefix'] = '('
            group['postfix'] = ')?'
            filters.append(group)

        struct = {'s': s, 'l': sl, 'filters': filters}

        if 'optional' in m2:
            struct['optional'] = True
            struct['prefix'] = '('
            struct['postfix'] = ')?'

        merge.append(struct)

    def mergeSingleGroup(self, filters, filtersGroup1, filtersGroup2, j, offset):
        filter1, filter2, group1, group2, maxRepetitions2, minRepetitions2, offset, repetitions1, repetitions2 = self.initSingleGroupMerge(filtersGroup1, filtersGroup2, j, offset)
        f = self.mergeFilter(filter1, filter2)
        maxR, minR, r = self.repetitions(maxRepetitions2, minRepetitions2, repetitions1, repetitions2)

        filter = {'filter': f, 'repetitions': r, 'minR': minR, 'maxR': maxR}

        if 'optional' in group1 or 'optional' in group2:
            filter['optional'] = True
            filter['prefix'] = '('
            filter['postfix'] = ')?'

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




