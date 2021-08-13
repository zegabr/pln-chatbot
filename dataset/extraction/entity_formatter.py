from sys import argv

file_name = argv[1]

entities = set()
entity_examples = {}
examples = set()

def add_word_to_entity(word, entity):
    if word not in examples:    
        examples.add(word)

        if entity not in entities:
            entities.add(entity)
            entity_examples[entity] = []
        entity_examples[entity].append(word)

def process_entity_classification():
    with open(file_name, 'r') as dataset:
        for line in dataset:
            line = line.rstrip()
            word_entity = line.split(',')
            entity = word_entity[-1]
            if entity != 'O':
                word_entity.pop()
                word = ''.join(word_entity).replace('"','')
                # print(word, entity)
                add_word_to_entity(word, entity)                

def print_entities_yml():
    print('entities:')
    for entity in entities:
        print(f'  - {entity}')

def print_examples_yml():
    print('nlu:')
    for entity in entity_examples:
        print(f'- lookup: {entity}')
        print('  examples: |')
        for example in entity_examples[entity]:
            print(f'    - {example}')
        print()


# main
process_entity_classification()
# print_entities_yml()
print_examples_yml()