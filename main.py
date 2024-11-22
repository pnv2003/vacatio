# from src import vacatio

# GRAMMAR_FILE = 'output/grammar.txt'
# SAMPLE_FILE = 'output/samples.txt'
# SENTENCE_FILE = 'input/sentences.txt'
# PARSE_FILE = 'output/parse-results.txt'

# print("Loading grammar...")
# grammar = vacatio.context_free_grammar()
# print("Grammar loaded")

# # dump grammar
# print("Dumping grammar...")
# grammar.save(GRAMMAR_FILE)
# print("Grammar saved to", GRAMMAR_FILE)

# # generate samples
# print("Generating samples...")
# grammar.generate(max_length=10, max_samples=10000, filename=SAMPLE_FILE)
# print("Samples saved to", SAMPLE_FILE)

# # parse sentences
# print("Parsing sentences...")
# with open(SENTENCE_FILE, 'r') as f:
#     sents = f.read().splitlines()

# grammar.parse_all(sents, filename=PARSE_FILE)
# print("Parse results saved to", PARSE_FILE)

import os
from underthesea import dependency_parse

with open('output/dep_parse.txt', 'w') as g:
    with open('input/questions.txt', 'r') as f:
        for line in f:
            q = line.strip()
            g.write('\n')
            g.write(str(dependency_parse(q)))