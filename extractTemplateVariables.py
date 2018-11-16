import json

extractVar = json.load(open('var.json'))

print(extractVar)
mylist = []

for item in extractVar:
    if '_TPL_' in item['name']:
        mylist.append(item)

print(mylist)