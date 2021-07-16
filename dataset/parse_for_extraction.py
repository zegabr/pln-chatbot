from os import supports_follow_symlinks
import nltk
from sys import argv
import csv
import pathlib
import json

nltk.download('punkt')

type_name = argv[1]
file_name = argv[2]

def get_entities(frames):
  entities = {}
  for frame in frames:
    for action in frame['actions']:
      if action['slot'] == 'intent':
        continue
      values = action[ 'values']
      for value in values:
        tokens = nltk.word_tokenize(value)
        entity = action['slot']
        for idx, word in enumerate(tokens):
          wordtype = ('B-' + entity) if idx == 0 else ('I-' + entity)
          print(idx, word, wordtype)
          entities[word] = wordtype
  return entities

def get_phrase_class_list(json_file):
  phrases_to_entities = []
  for item in json_file:
    if len(item['services']) > 1 or type_name not in item['services']:
      continue
    for turn in item['turns']:
      if turn['speaker'] == 'SYSTEM':
        continue
      splitted_text = nltk.word_tokenize(turn['utterance'])
      entities = get_entities(turn['frames'])
      for word in splitted_text:
        if word in entities:
          phrases_to_entities.append([word, entities[word]])
        else:
          phrases_to_entities.append([word, 'O'])
      phrases_to_entities.append(['', ''])
  return phrases_to_entities

if __name__ == '__main__': 
  count = 0 
  f = open(f'./extraction/{file_name}_dataset.csv', 'w')
  writer = csv.writer(f)
  writer.writerow(['Phrase', 'Entity'])
  for path in pathlib.Path(f'../dstc8-schema-guided-dialogue/{file_name}').iterdir():
    if path.is_file() and not path.match('*schema.json'):
      current_file = open(path, "r")
      json_file = json.loads(current_file.read())
      phrase_class_list = get_phrase_class_list(json_file)
      for phrase_class in phrase_class_list:
        writer.writerow(phrase_class)
  current_file.close()
  f.close()
