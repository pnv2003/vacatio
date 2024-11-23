from src import vacatio

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

questions = []
with open('input/questions.txt', 'r', encoding='utf-8') as f:
    questions = f.read().splitlines()

grammar = vacatio.dependency_grammar()
grammar.parse_all(questions)