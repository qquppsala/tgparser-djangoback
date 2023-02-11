import json

with open('channel_messages.json') as inf:
    data =json.load(inf)

name = 'OZON'
comment_list = list(data[name].keys())

print(list(data[name]['973']))
print(str(data[name]['973'][0]))
print(data[name]['973'][1])
print(data[name]['973'][2])
