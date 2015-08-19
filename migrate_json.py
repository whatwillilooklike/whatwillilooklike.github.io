import json

j = json.load(open('json_dump.json', 'r'))
for i in range (len(j['result'])):
    imgur_images = j['result'][i]['media_json']['imgur_images']
    j['result'][i]['photos'] = imgur_images
    del j['result'][i]['media_json']
    del j['result'][i]['adult_content']
    del j['result'][i]['media_embed_json']

json.dump(j, open('json_dump_new.json', 'w'))
