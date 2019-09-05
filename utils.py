class Utils:
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
        return currentFilter, hc, isFilter, isHardCode, savefilter

    def savingFilter(self, filter, filters, hc, rep):
        f = {'filter': filter, 'repetitions': rep, 'hc': hc}
        filters.append(f)

    def regexString(self, m):
        regex = ''
        for f in m:
            if f['repetitions'] > 0:
                regex = regex + f['filter'] + '{' + str(f['repetitions']) + '}' + f['hc']
            else:
                regex = regex + f['filter'] + f['hc']

        return regex
