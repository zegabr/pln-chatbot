from sys import argv
import csv
import pathlib
import json

type_name = argv[1]
file_name = argv[2]

def get_entities(json_file):
    word_to_entity = {}
    for item in json_file:
        if type_name not in item['services'] or len(item['services']) > 1:
            continue
        for turn in item['turns']:
          if turn['speaker'] == 'SYSTEM':
              continue
          for frame in turn['frames']:
              if frame['service'] != type_name:
                continue
              state = frame['state']
              slot_values = state['slot_values']
              for entity in slot_values.keys():
                  for value in slot_values[entity]:
                      words = value.split()
                      for i in range(len(words)):
                          if i == 0:
                              word_to_entity[value] = 'B-' + entity
                          else:
                              word_to_entity[value] = 'I-' + entity
    return word_to_entity

def fix_punct(text):
    text = text.replace('.',' . ')
    text = text.replace(',',' , ')
    text = text.replace('?',' ? ')
    text = text.replace(';',' ; ')
    text = text.replace('!',' ! ')
    text = text.replace('"',' " ')
    return text

def empty(word):
    for i in range(len(word)):
        c = word[i]
        if c != ' ':
            return False
    return word != ''

def format_stuff(json_file, word_to_entity):
    phrases_to_entities = []
    for item in json_file:
        if type_name not in item['services'] or len(item['services']) > 1:
            continue
        for turn in item['turns']:
            if turn['speaker'] == 'SYSTEM':
                continue
            text = turn['utterance']
            text = fix_punct(text)
            text = text.replace('  ', ' ')
            text = text.split()

            entities = []
            for word in text:
                if empty(word):
                    continue
                if word in word_to_entity:
                    entities.append(word_to_entity[word])
                else:
                    entities.append('O')
            phrases_to_entities.append((text, entities))
    return phrases_to_entities

if __name__ == '__main__': 
  count = 0 
  f = open(f'{file_name}.csv', 'w')
  writer = csv.writer(f)
  writer.writerow(['Phrase', 'Entity'])
  for path in pathlib.Path("dstc8-schema-guided-dialogue/train").iterdir():
    if path.is_file() and not path.match('*schema.json'):
      current_file = open(path, "r")
      json_file = json.loads(current_file.read())
      word_to_entity = get_entities(json_file)
      formatted = format_stuff(json_file, word_to_entity)
      if len(formatted) > 0:
          for phrase in formatted:
              text_array = phrase[0]
              entity_array = phrase[1]
              tam = len(text_array)
              for i in range(tam):
                  writer.writerow([text_array[i], entity_array[i]])
              writer.writerow(['',''])
  current_file.close()
  f.close()
