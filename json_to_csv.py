import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import json
import csv

def get_string_after(substr, s):
    idx = s.find(substr) + len(substr)
    return s[idx:]

def image_id_from_url(imgur_url):
    return get_string_after('imgur.com/', imgur_url)

j = json.load(open('json_dump.json', 'r'))
# print j
data = j['result']
columns = data[0].keys()
columns.remove('permalink')

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
                image_ids = [image_id_from_url(url) for url in val]
                val = ','.join(image_ids)
            row.append(val)
        csvwriter.writerow(row)
