import sys
import json
import yaml

js = json.loads(open('intents_to_utterance_fixed.json').read())

# f = open('nlu.yml', 'w')
# yaml.dump(js, f, allow_unicode=True)

def print_examples_yml(a):
    print('nlu:')
    for intent in a:
        print(f'- intent: {intent}')
        print('  examples: |')
        for example in a[intent]:
            print(f'    - {example}')
        print()

print_examples_yml(js['SYSTEM'])
