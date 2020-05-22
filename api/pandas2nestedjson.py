import pandas as pd
x = pd.read_csv('sample.csv')

y=x.groupby(['continent_ocean','country','state_province','city','county'])[['id']]

grouped = y.count()


levels = len(grouped.index.levels)
dicts = [{} for i in range(levels)]
last_index = None


for index,value in grouped.itertuples():

    if not last_index:
        last_index = index

    for (ii,(i,j)) in enumerate(zip(index, last_index)):
        if not i == j:
            ii = levels - ii -1
            dicts[:ii] =  [{} for _ in dicts[:ii]]
            break

    for i, key in enumerate(reversed(index)):
        dicts[i][key] = value
        value = dicts[i]

    last_index = index
    

import json
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_json'):
            return obj.to_json(orient='records')
        return json.JSONEncoder.default(self, obj)

with open('result.json', 'w') as fp:
    json.dump(dicts[-1], fp, cls=JSONEncoder)
