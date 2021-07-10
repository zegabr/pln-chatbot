from sys import argv
import csv
import pathlib
import json

type_name = argv[1]
file_name = argv[2]

user = {}
intents = set()

intent_mapper = {
  'NEGATE': 'NEGATE',
  'NEGATE_INTENT': 'NEGATE',
  'REQUEST_ALTS': 'REQUEST_ALTS',
  'GOODBYE': 'GOODBYE',
  'REQUEST': 'REQUEST',
  'THANK_YOU': 'THANK_YOU',
  'AFFIRM': 'AFFIRM',
  'AFFIRM_INTENT': 'AFFIRM',
  'SELECT': 'SELECT',
  'INFORM': 'INFORM',
  'INFORM_INTENT': 'INFORM'
}

def filter_itents(json_file, file_name):
  for item in json_file:
      if type_name not in item['services']:
        continue
      for turn in item['turns']:
          if turn['speaker'] == 'SYSTEM':
              continue
          text = turn['utterance']
          intent = 'other'
          for frame in turn['frames']:
              if frame['service'] != type_name:
                continue
              for action in frame['actions']:
                  intent = action['act']
                  # if action['slot'] in {'intent' , ''}:
                      # intent = action['act']
                      # break
                  if text not in user:
                    user[text] = set()
                  user[text].add(intent_mapper[intent])
                  intents.add(intent)

def intent_group():
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
  

if __name__ == '__main__': 
  for path in pathlib.Path("dstc8-schema-guided-dialogue/train").iterdir():
    if path.is_file() and not path.match('*schema.json'):
      current_file = open(path, "r")
      json_file = json.loads(current_file.read())
      filter_itents(json_file, path)
      current_file.close()
  f = open(f'{file_name}.csv', 'w')
  writer = csv.writer(f)
  writer.writerow(['Phrase', 'Intent'])
  for (phrase, intent_list) in user.items():
    for intent in intent_list:
      writer.writerow([phrase, intent])
  f.close()
print(intents)