import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import json
import csv

j = json.load(open('json_dump.json', 'r'))
# print j
data = j['result']
columns = data[0].keys()

with open('json_dump.csv', 'w') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(columns)  # headers
    for entry in data:
        print entry
        row = []
        for column in columns:
            val = entry[column]
            if column == 'gender':
                # for javascript, need gender to be lowercase
                val = str(val).lower()
            if column == 'photos':
                val = ','.join(val)
            row.append(val)
        csvwriter.writerow(row)
