#!/usr/bin/env python3

from datetime import date
import requests
from sqlthemall.json_importer import SQLThemAll

url = 'https://pomber.github.io/covid19/timeseries.json'
o = requests.get(url).json()
l = []
for k in o.keys():
    for i in [d for d in o[k]]:
        i['country'] = k
        l.append(i)

for i in l:
    i['date'] = date(*[int(i) for i in i['date'].split('-')])
s = SQLThemAll('postgresql://api:apipw@localhost:5432/storage', simple=True, root_table='dates', quiet=False, verbose=True)
s.importJSON(l)

