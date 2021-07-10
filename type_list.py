import pathlib
import json

type_dict = {}

def process_object(json_file):
  for obj in json_file:
    for type in obj['services']:
      type_dict[type] = type_dict[type] + 1 if type in type_dict else 0

for path in pathlib.Path("dstc8-schema-guided-dialogue/train").iterdir():
  if path.is_file() and not path.match('*schema.json'):
    current_file = open(path, "r")
    json_file = json.loads(current_file.read())
    process_object(json_file)
    current_file.close()

sorted_types = []
for (type, amount) in type_dict.items():
  sorted_types.append((type, amount))

sorted_types.sort(key=lambda a: a[1], reverse=True)
for (type, amount) in sorted_types:
  print(f'{type}: {amount}')
