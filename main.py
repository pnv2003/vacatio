from src import vacatio

GRAMMAR_FILE = 'output/grammar.txt'
SAMPLE_FILE = 'output/samples.txt'
SENTENCE_FILE = 'input/sentences.txt'
PARSE_FILE = 'output/parse-results.txt'

grammar = vacatio.context_free_grammar()

# dump grammar
grammar.save(GRAMMAR_FILE)

# generate samples
grammar.generate(max_length=10, max_samples=10000, filename=SAMPLE_FILE)

# parse sentences
with open(SENTENCE_FILE, 'r') as f:
    sents = f.read().splitlines()

grammar.parse_all(sents, filename=PARSE_FILE)