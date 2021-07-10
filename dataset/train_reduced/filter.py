from sys import argv
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
                if action['slot'] == 'intent':
                    intent = action['act']
        user['text'].append(text)
        user['intent'].append(intent)
        intents.add(intent)
        print(text, intent)

print(intents)
