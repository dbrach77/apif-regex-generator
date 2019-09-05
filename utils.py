class Utils:
    maxLength = 16
    isHardCode = False
    sLenght = 0
    def regexMap(self, s):
        isHardCode = False
        endOfString = False
        filter = ''
        hc = ''
        currentFilter = ''

        rep = 0
        l = 0
        filters = []

        for n in s:
            l = l + 1
            currentFilter, hc, isFilter, isHardCode, savefilter = self.filterOrHardcode(currentFilter, hc, isHardCode,n)
            filter, rep = self.repetitionsAndFilter(currentFilter, filter, isHardCode, rep)
            filter, hc, isHardCode, rep = self.saveFilter(currentFilter, endOfString, filter, filters, hc, isFilter,isHardCode, l, rep, s, savefilter)

        self.sLenght = len(s)
        return filters

    def saveFilter(self, currentFilter, endOfString, filter, filters, hc, isFilter, isHardCode, l, rep, s, savefilter):
        # se sono alla fine devo storare
        if l == len(s):
            endOfString = True
        # se ho un filtro e il nuovo è diverso salvo il filtro
        if filter != currentFilter or isHardCode == True and isFilter == True:
            savefilter = True
        if savefilter == True:
            self.savingFilter(filter, filters, hc, rep)
            filter = currentFilter
            rep = 1
            hc = ''
            isHardCode = False
        if endOfString == True:
            self.savingFilter(currentFilter, filters, hc, rep)
            filter = ''
        return filter, hc, isHardCode, rep

    def repetitionsAndFilter(self, currentFilter, filter, isHardCode, rep):
        if not isHardCode:
            if filter == '':
                filter = currentFilter
            # se trovo un filtro ed è lo stesso di prima allora incremento il contatore
            if filter == currentFilter:
                rep = rep + 1
        return filter, rep

    def filterOrHardcode(self, currentFilter, hc, isHardCode, n):
        isFilter = False
        savefilter = False
        if 'a' <= n <= 'z':
            currentFilter = '[a-z]'
            isFilter = True
        elif 'A' <= n <= 'Z':
            currentFilter = '[A-Z]'
            isFilter = True
        elif '0' <= n <= '9':
            currentFilter = '[0-9]'
            isFilter = True
        else:
            hc = hc + n
            isHardCode = True
            self.isHardCode = True
        return currentFilter, hc, isFilter, isHardCode, savefilter

    def savingFilter(self, filter, filters, hc, rep):
        f = {'filter': filter, 'repetitions': rep, 'hc': hc}
        filters.append(f)

    def regexString(self, m, forced):
        regex = ''
        if not forced and (self.sLenght > self.maxLength or not self.isHardCode and len(m) > 2): #:self.sLenght/2:
            regex = '.*'
        elif not forced and self.isHardCode == True:
            groups = 0
            tempregex = ''
            fCount = 0
            for f in m:
                fCount = fCount + 1
                if 0 < f['repetitions']:
                    groups = groups + 1
                    if groups > 2:
                       tempregex = '.*' + f['hc']
                    else:
                        tempregex = tempregex + f['filter'] + '{' + str(f['repetitions']) + '}' + f['hc']

                    if f['hc'] != '' or fCount == len(m):
                        groups = 0
                        regex = regex + tempregex
                        tempregex = ''

                else:
                    regex = regex + f['filter'] + f['hc']
        else:
            for f in m:
                if 0 < f['repetitions']:
                    regex = regex + f['filter'] + '{' + str(f['repetitions']) + '}' + f['hc']
                #elif f['repetitions'] >= self.maxLength:
                #    regex = regex + f['filter'] + '*' + f['hc']
                else:
                    regex = regex + f['filter'] + f['hc']


        return regex
