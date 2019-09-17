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
        for m in s:
            i = i +1
            if 'optional' in m and not '(' in regex:
                regex = regex + '('

            regex = regex + self.singleGroupRegex(m)

            if i == len(s) and 'optional' in m and regex!= '.*':# and not 'hc' in m:
                regex = regex +')?'

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

            if 'hc' in m1:
                filters = []
                hc = {'hc': m1['hc']}
                if 'optional' in m2:
                    hc['optional'] = True
                merge.append(hc)

        for l in range(diffFilters):
            m = longest[l+offset]
            if 's' in m:
                m['optional'] = True
                merge.append(m)
            if 'hc' in m:
                filters = []
                merge.append({'hc': m['hc'],'optional': True})
        return merge

    def mergeFilters(self, filters, m1, m2, merge):
        if len(m1['s']) > len(m2['s']):
            sl = len(m1['s'])
            s = m1['s']
        else:
            sl = len(m2['s'])
            s = m2['s']
        filtersGroup1 = m1['filters']
        filtersGroup2 = m2['filters']
        lengthDifference, minLength, longestStruct = self.longestMinDifference(filtersGroup1, filtersGroup2)
        offsetInner = 0
        for j in range(minLength):
            offsetInner = offsetInner + 1
            g1 = filtersGroup1[j]
            g2 = filtersGroup2[j]
            f1 = g1['filter']
            f2 = g2['filter']
            r1 = g1['repetitions']
            r2 = g2['repetitions']
            minR2 = g2['minR']
            maxR2 = g2['maxR']

            if f1 == f2:
                f = f1
            elif f1 in f2:
                f = f2
            else:
                f = f1 + f2

            r = 0
            minR = 0
            maxR = 0

            if (r2 == 0):
                if r1 < minR2:
                    minR = r1
                else:
                    minR = minR2

                if r1 > maxR2:
                    maxR = r1
                else:
                    maxR = maxR2

            else:
                if r1 == r2:
                    r = r1
                elif r1 < r2:
                    minR = r1
                    maxR = r2
                else:
                    minR = r2
                    maxR = r1

            filter = {'filter': f, 'repetitions': r, 'minR': minR, 'maxR': maxR}
            if 'optional' in g1 or 'optional' in g2:
                filter['optional'] = True

            filters.append(filter)
        for k in range(lengthDifference):
            g = longestStruct[k + offsetInner]
            f = g['filter']
            r = g['repetitions']
            g['optional'] = True
            filters.append(g)
        struct = {'s': s, 'l': sl, 'filters': filters}
        if 'optional' in m2:
            struct['optional'] = True
        merge.append(struct)

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




