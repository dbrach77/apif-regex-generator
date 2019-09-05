class Utils:
    def regexMap(self, s):
        ishc = False
        storefilter = False
        store = False
        isFilter = False
        filter =''
        hc = ''
        currentFilter = ''

        rep = 0
        l = 0
        filters = []

        for n in s:
            l = l + 1
            isFilter = False
            storefilter = False
            if 'a' <= n and n <='z':
                currentFilter = '[a-z]'
                isFilter = True
            elif 'A' <= n and n <='Z':
                currentFilter = '[A-Z]'
                isFilter = True
            elif '0' <= n and n <='9':
                currentFilter = '[0-9]'
                isFilter = True
            else:
                hc = hc + n
                ishc = True

            if ishc == False:
                if filter == '':
                    filter = currentFilter
                #se trovo un filtro ed è lo stesso di prima allora incremento il contatore
                if filter == currentFilter:
                    rep = rep + 1

            if ishc == True and isFilter == True:
                storefilter = True

            #se sono alla fine devo storare
            if l == len(s):
                store = True
            #se ho un filtro e il nuovo è diverso salvo il filtro
            if filter != currentFilter: #and l == len(s):
                storefilter = True

            if storefilter == True:
                f = {'filter':filter,'repetitions':rep,'hc':hc}
                filters.append(f)
                filter = currentFilter
                rep = 1
                hc = ''
                ishc = False

            if store == True:
                f = {'filter':currentFilter,'repetitions':rep,'hc':hc}
                filters.append(f)
                filter = ''



        return filters

    def regexString(self,m):
        regex = ''
        for f in m:
                if f['repetitions'] > 0:
                    regex = regex + f['filter']+'{'+str(f['repetitions'])+'}'+f['hc']
                else:
                    regex = regex + f['filter']+ f['hc']

        return regex


