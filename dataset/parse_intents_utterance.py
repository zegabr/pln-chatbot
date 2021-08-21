from sys import argv
import csv
import pathlib
import json

type_name = argv[1]
file_name = argv[2]

users = {}
users['USER'] = {}
users['SYSTEM'] = {}
entities = set()

intent_mapper = {
  'REQ_MORE': -7,
  'NOTIFY_FAILURE': -6,
  'NOTIFY_SUCCESS': -5,
  'CONFIRM': -4,
  'INFORM_COUNT': -3,
  'OFFER': -2,
  'OFFER_INTENT': -1,
  'NEGATE': 0,
  'NEGATE_INTENT': 1,
  'REQUEST_ALTS': 3,
  'GOODBYE': 4,
  'REQUEST': 6,
  'THANK_YOU': 7,
  'AFFIRM': 8,
  'AFFIRM_INTENT': 9,
  'SELECT': 10,
  'INFORM': 11,
  'INFORM_INTENT': 12
}

def compare_intents(intent_a, intent_b):
  if intent_mapper[intent_a] >= intent_mapper[intent_b]:
    return intent_a
  return intent_b

def filter_itents(json_file, file_name):
  for item in json_file:
    # if type_name not in item['services']:
    if len(item['services']) > 1 or type_name not in item['services']:
      continue
    for turn in item['turns']:
      # if turn['speaker'] == 'SYSTEM':
      #     continue
      speaker = turn['speaker']
      text = turn['utterance']
      intent = 'NEGATE'
      for frame in turn['frames']:
        if frame['service'] != type_name or len(frame['actions']) > 1:
          intent = None
          continue
        for action in frame['actions']:
          intent = '%s_%s' % (action['act'].lower(), action['slot'])
          if action['values'] and action['slot'] != 'party_size':
            entities.add(action['slot'])
            # text = text.lower().replace(action['values'][0].lower(), '[%s](%s)' % (action['values'][0], action['slot']))
            text = text.replace(action['values'][0], '[%s](%s)' % (action['values'][0], action['slot']))
      if not intent:
        continue
      if intent not in users[speaker]:
        users[speaker][intent] = set()
      users[speaker][intent].add(text)

def find_bugs(phrases):
  for phrase in phrases:
    op = 0
    for letter in phrase:
      if letter == '[':
        op += 1
      elif letter == ']':
        op -= 1
      if op > 1:
        print(phrase)
        break
  
if __name__ == '__main__': 
  for path in pathlib.Path(f'../dstc8-schema-guided-dialogue/{file_name}').iterdir():
    if path.is_file() and not path.match('*schema.json'):
      current_file = open(path, "r")
      json_file = json.loads(current_file.read())
      filter_itents(json_file, path)
      current_file.close()
  # print(users)
  unique_user_phrases = {}
  for user, intents in users.items():
    if user not in unique_user_phrases:
      unique_user_phrases[user] = {}
    for intent, phrases in intents.items():
      print('\t- ', intent)
      unique_user_phrases[user][intent] = list(phrases)
      unique_user_phrases[user][intent].sort()
      # find_bugs(phrases)
    print('------ end of %s --------' % user)
  f = open('intents_to_utterance.json', 'w')
  json.dump(unique_user_phrases, f, indent=2)
  print(entities)