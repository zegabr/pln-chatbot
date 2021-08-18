import sys
import json
import yaml
from sys import argv

filter = argv[1]

js = json.loads(open('intents_to_utterance.json').read())

f = open('%s_intent.yml' % filter.lower(), 'w')
# yaml.dump(js, f, allow_unicode=True)

def print_examples_yml(a):
    f.write('nlu:\n')
    for intent in a:
        f.write(f'- intent: {intent}\n')
        f.write('  examples: |\n')
        for example in a[intent]:
            f.write(f'    - {example}\n')
        f.write('\n')

print_examples_yml(js[filter])
