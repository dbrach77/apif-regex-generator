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

            f = {'filter': filter, 'repetitions': rep}

            if filter != currentFilter:
                filters.append(f)
                filter = currentFilter
                rep = 1

            if l == len(s):
                filters.append(f)

        #self.sLenght = len(s)
        struct = {'s':s,'l':len(s),'filters':filters}
        return struct
        #return filters


    def regex(self, s):
        regex =''
        #if self.isHardCode == True:
        for m in s:
            regex = regex + self.regexString(m)
        """else:
            m = s
            regex = self.regexString(m)"""
        return regex

    #get the regex from the list of filters
    def regexString(self, m):
        regex = ''

        if 's' in m:
            s = m['s']
            sLenght =  m['l']
            filters = m['filters']
            if (sLenght > self.maxLength or (sLenght > 1 and len(filters) > sLenght/2)):
                regex = '.*'
            else :
                for f in filters:
                    if 1 < f['repetitions']:
                        regex = regex + '[' + f['filter'] +']' +'{' + str(f['repetitions']) + '}'
                    else:
                        regex = regex + '[' + f['filter'] +']'

        if 'hc' in m:
            regex = regex + m['hc']
        return regex

    def merge(self,struct1,struct2):
        regex =''
        l = 0
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
            groups = 0
            m1 = struct1[i]
            m2 = struct2[i]
            s1 = self.regexString(m1)
            s2 = self.regexString(m2)

            if s1 == '.*' or s2 == '.*':
                regex = regex + '.*'
            elif s1 == s2:
                regex = regex + s1
                groups = groups + 1
            else:
                regex = self.mergeGroup(groups, m1, m2, regex)

        for j in range(diffFilters):
            m = longest[j+offset]
            s = self.regexString(m)
            regex = regex + s1

        return regex

    def mergeGroup(self, groups, m1, m2, regex):
        if len(m1['s']) > len(m2['s']):
            sl = len(m1['s'])
        else:
            sl = len(m2['s'])
        filters1 = m1['filters']
        filters2 = m2['filters']
        if len(filters1) < len(filters2):
            lf = len(filters1)
            diffFilters = len(filters2) - lf
            longest = filters2
        else:
            lf = len(filters2)
            diffFilters = len(filters1) - lf
            longest = filters1
        offset = 0
        tempregex = ''
        for j in range(lf):
            offset = offset + 1
            g1 = filters1[j]
            g2 = filters2[j]
            f1 = g1['filter']
            f2 = g2['filter']
            r1 = g1['repetitions']
            r2 = g2['repetitions']
            if r1 < r2:
                min = r1
                diff = r2 - r1
                follow = '[' + f2 + ']'
            else:
                min = r2
                diff = r1 - r2
                follow = '[' + f1 + ']'
            if f1 != f2:
                filter = '[' + f1 + f2 + ']'
            else:
                filter = '[' + f1 + ']'

            if diff > 0:
                tempregex = tempregex + filter + '{' + str(min)+','+ str(min+diff) + '}' #+ '(' + follow + '{' + str(diff) + '}' + ')?'
                groups = groups + 1
            else:
                tempregex = tempregex + filter + '{' + str(min) + '}'
                groups = groups + 1

        for k in range(diffFilters):
            g = longest[j + offset]
            f = g['filter']
            r = g['repetitions']
            filter = '[' + f + ']'
            #tempregex = tempregex + '(' + filter + '{' + str(r) + '}' + ')?'
            tempregex = tempregex + '(' + filter + '{' + str(r) + '}' + ')?'
            groups = groups + 1
        # regex = regex + '[' + s1 + s2 + ']'
        print(sl / 2)
        print(groups)
        if groups >  sl / 2:
            regex = regex + '.*'
        else:
            regex = regex + tempregex
        return regex




