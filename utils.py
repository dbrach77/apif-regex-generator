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

            if not isHardCode:
                if filter == '':
                    filter = currentFilter
                # se trovo un filtro ed è lo stesso di prima allora incremento il contatore
                if filter == currentFilter:
                    rep = rep + 1

            # se sono alla fine devo storare
            if l == len(s):
                endOfString = True
            # se ho un filtro e il nuovo è diverso salvo il filtro
            if filter != currentFilter or isHardCode == True and isFilter == True:
                savefilter = True

            if savefilter == True:
                self.saveFilter(filter, filters, hc, rep)
                filter = currentFilter
                rep = 1
                hc = ''
                isHardCode = False

            if endOfString == True:
                self.saveFilter(currentFilter, filters, hc, rep)
                filter = ''

        return filters

    def saveFilter(self, filter, filters, hc, rep):
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
