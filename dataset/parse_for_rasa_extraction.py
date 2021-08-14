from os import supports_follow_symlinks
from sys import argv
import csv
import pathlib
import json


type_name = argv[1]
file_name = argv[2]

entities = {}

def get_entities(frames):
  for frame in frames:
    for action in frame['actions']:
      if action['slot'] == 'intent':
        continue
      values = action[ 'values']
      entity = action['slot']
      if entity not in entities:
        entities[entity] = set()
      for value in values:
        entities[entity].add(value)

def get_entities_from_json(json_file):
  for item in json_file:
    if len(item['services']) > 1 or type_name not in item['services']:
      continue
    # print(item['services'])
    for turn in item['turns']:
      if turn['speaker'] == 'SYSTEM':
        continue
      get_entities(turn['frames'])

def print_entities_yml():
    print('entities:')
    for entity in entities:
        print(f'  - {entity}')

def print_examples_yml():
    print('nlu:')
    for entity in entities:
        print(f'- lookup: {entity}')
        print('  examples: |')
        for example in entities[entity]:
            print(f'    - {example}')
        print()

if __name__ == '__main__': 
  # count = 0 
  # f = open(f'./extraction/{file_name}_dataset.csv', 'w')
  # writer = csv.writer(f)
  # writer.writerow(['Phrase', 'Entity'])
  for path in pathlib.Path(f'../dstc8-schema-guided-dialogue/{file_name}').iterdir():
    if path.is_file() and not path.match('*schema.json'):
      current_file = open(path, "r")
      json_file = json.loads(current_file.read())
      get_entities_from_json(json_file)
  # print(entities)
  print_examples_yml()
  # print_entities_yml()
      # for phrase_class in phrase_class_list:
        # writer.writerow(phrase_class)
  # current_file.close()
  # f.close()
