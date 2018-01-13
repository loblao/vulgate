import requests
import time
import sys
import os

def getUA(i):
    ualist = ('Pater', 'noster', 'qui', 'es', 'in', 'caelis',
             'sanctificetur', 'nomen', 'tuum', 'adveniat', 'regnum',
             'tuum', 'fiat', 'voluntas', 'tua', 'sicut', 'in', 'caelo',
             'et', 'in', 'terra', 'panem', 'nostrum', 'quotidianum',
             'da', 'nobis', 'hodie', 'dimitte', 'nobis', 'debita',
             'nostra', 'sicut', 'et', 'nos', 'dimittimus', 'debitoribus',
             'nostris', 'et', 'ne', 'nos', 'inducas', 'in', 'tentationem',
             'sed', 'libera', 'nos', 'a', 'malo',

             'Ave', 'Maria', 'gratia', 'plena', 'Dominus',
             'tecum', 'benedicta', 'tu', 'in', 'mulieribus',
             'et', 'benedictus', 'fructus', 'ventris', 'tui',
             'Iesus', 'Sancta', 'Maria', 'Mater', 'Dei', 'ora',
             'pro', 'nobis', 'peccatoribus', 'nunc', 'et', 'in',
             'hora', 'mortis', 'nostrae', 'Amen',

             'Gloria', 'Patri', 'et', 'Filio', 'et', 'Spiritui', 'Sancto',
             'sicut', 'erat', 'in', 'principio', 'et', 'nunc', 'et', 'semper',
             'et', 'in', 'saecula', 'saeculorum', 'Amen')
    if i < len(ualist):
        return ualist[i]

    return ('Verbum Domini', 'Deo Gratias')[i % 2]

i = 0
for path in sys.stdin.readlines():
    path = path.strip()
    if not path:
        continue

    i += 1
    headers = {'User-Agent': getUA(i)}
    path = path[1:]
    name, index = path.rsplit('/', 1)[-1].rsplit('_', 1)
    filename = 'original/' + path.rsplit('/', 1)[0] + '/' + name + '/' + index

    if os.path.isfile(filename):
        continue

    os.system('mkdir -p ' + path.rsplit('/', 1)[0] + '/' + name)
    r = requests.get('http://vulgate.org/' + path, headers=headers)
    with open(filename, 'wb') as f:
        f.write(r.text.encode('latin-1'))

    if i % 5 == 0:
        print i, filename
        time.sleep(0.5)
