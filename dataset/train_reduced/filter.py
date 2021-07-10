from sys import argv
import csv
import json

filename = argv[1]

f = open(filename, 'r')

obj = json.loads(f.read())

user = {'text':[], 'intent':[]}
intents = set()

for item in obj:
    for turn in item['turns']:
        if turn['speaker'] == 'SYSTEM':
            continue
        text = turn['utterance']
        intent = 'other'
        for frame in turn['frames']:
            for action in frame['actions']:
                intent = action['act']
                # if action['slot'] in {'intent' , ''}:
                    # intent = action['act']
                    # break
                user['text'].append(text)
                user['intent'].append(intent)
                intents.add(intent)
        if intent == 'other':
            print(text, intent)

f.close()

f = open('coisadecentepelocristo.csv', 'w')
writer = csv.writer(f)
for i in range(len(user['text'])):
    writer.writerow([user['text'][i],user['intent'][i]])

f.close()

finalObj = {}

for i in range(len(user['text'])):
    currKey = user['text'][i]
    currIntent = user['intent'][i]

    if currKey not in finalObj:
        finalObj[currKey] = set()
    finalObj[currKey].add(currIntent)

print(len(finalObj))
i = 0
for item in finalObj.items():
    if('INFORM' in item[1] and len(item[1]) == 1):
        i += 1
print(i)
