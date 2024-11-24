from src.logic import LogicalFormulator
from src.procedure import ProcedureExecutor
from src.relation import RelationExtractor
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

questions = []
with open('input/questions.txt', 'r', encoding='utf-8') as f:
    questions = f.read().splitlines()

grammar = vacatio.dependency_grammar()
grammar.save()
dep_lists = grammar.parse_all(questions, save=True)

# print(dep_lists)

extractor = RelationExtractor(vacatio.extract_relations, save=True)
relation_lists = extractor.extract_all(dep_lists)

# print(relation_lists)

logical_formulator = LogicalFormulator(
    logicalizer=vacatio.logical_formulate,
    save=True
)

lfs = logical_formulator.logicalize_all(relation_lists)

# print(lfs)

executor = ProcedureExecutor(vacatio.procedural_formulate, save=True)
procedures = executor.proceduralize_all(lfs)

# print(procedures)

print(executor.execute(procedures[5]))
