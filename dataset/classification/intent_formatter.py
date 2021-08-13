from sys import argv

file_name = argv[1]

intents = set()
intent_examples = {}
examples = set()

def add_phrase_to_intent(phrase, intent):
    if phrase not in examples:    
        examples.add(phrase)

        if intent not in intents:
            intents.add(intent)
            intent_examples[intent] = []
        intent_examples[intent].append(phrase)

def process_intent_classification():
    with open(file_name, 'r') as dataset:
        for line in dataset:
            line = line.rstrip()
            phrase_intent = line.split(',')
            intent = phrase_intent[-1]
            phrase_intent.pop()
            phrase = ''.join(phrase_intent).replace('"','')
            add_phrase_to_intent(phrase, intent)                

def print_intents_yml():
    print('intents:')
    for intent in intents:
        print(f'  - {intent}')

def print_examples_yml():
    print('nlu:')
    for intent in intent_examples:
        print(f'- intent: {intent}')
        print('  examples: |')
        for example in intent_examples[intent]:
            print(f'    - {example}')
        print()


# main
process_intent_classification()
# print_intents_yml()
print_examples_yml()