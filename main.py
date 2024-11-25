import re
from src import vacatio

# GRAMMAR_FILE = 'output/grammar.txt'
# SAMPLE_FILE = 'output/samples.txt'
# SENTENCE_FILE = 'input/sentences.txt'
# PARSE_FILE = 'output/parse-results.txt'

# grammar = vacatio.context_free_grammar()
# grammar.save(GRAMMAR_FILE)
# grammar.generate(max_length=10, max_samples=10000, filename=SAMPLE_FILE)
# with open(SENTENCE_FILE, 'r') as f:
#     sents = f.read().splitlines()
# grammar.parse_all(sents, filename=PARSE_FILE)

DATABASE_FILE = 'input/database.txt'
QUESTION_FILE = 'input/questions.txt'
RELATION_FILE = 'output/p2-q-3.txt'
LOGICAL_FILE = 'output/p2-q-4.txt'
ANSWER_FILE = 'output/p2-q-5.txt'

questions = []
with open(QUESTION_FILE, 'r', encoding='utf-8') as f:
    questions = f.read().splitlines()

db = {'TOUR': [], 'TIME': [], 'RUN-TIME': [], 'BY': []}
with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
    content = f.read()
    tour_pattern = re.compile(r'\(TOUR (\w+) (\w+)\)')
    time_pattern = re.compile(r'\(DTIME (\w+) (\w+) "([^"]+)"\) \(ATIME \w+ (\w+) "([^"]+)"\)')
    runtime_pattern = re.compile(r'\(RUN-TIME (\w+) (\w+) (\w+) ([\d:]+ \w+)\)')
    by_pattern = re.compile(r'\(BY (\w+) (\w+)\)')

    db['TOUR'] = tour_pattern.findall(content)
    db['TIME'] = time_pattern.findall(content)
    db['RUN-TIME'] = runtime_pattern.findall(content)
    db['BY'] = by_pattern.findall(content)

grammar = vacatio.dependency_grammar()
grammar.save()
dep_lists = grammar.parse_all(questions, save=True)

with open(RELATION_FILE, 'w', encoding='utf-8') as f:
    f.write('')

with open(LOGICAL_FILE, 'w', encoding='utf-8') as f:
    f.write('')

with open(ANSWER_FILE, 'w', encoding='utf-8') as f:
    f.write('')

for i, deps in enumerate(dep_lists):

    with open(RELATION_FILE, 'a', encoding='utf-8') as f:

        relations = vacatio.relationalize(deps)
        f.write('-----------------------------------\n')
        f.write(f'Relationalizing: {questions[i]}\n')
        f.write('-----------------------------------\n')
        f.write(f'{relations}\n\n')

    with open(LOGICAL_FILE, 'a', encoding='utf-8') as f:
    
        lf = vacatio.logicalize(relations)
        proc = vacatio.proceduralize(lf)
        f.write('-----------------------------------\n')
        f.write(f'Logicalizing and Proceduralizing: {questions[i]}\n')
        f.write('-----------------------------------\n')
        f.write(f'{lf}\n')
        f.write(f'{proc}\n\n')

    with open(ANSWER_FILE, 'a', encoding='utf-8') as f:
            
        answer = vacatio.answer(proc, db)
        f.write('-----------------------------------\n')
        f.write(f'Answering: {questions[i]}\n')
        f.write('-----------------------------------\n')
        f.write(f'{answer}\n\n')
