from typing import List
from src.dep import Dependency

QUERY_MAP = {
    'bao_nhiêu': 'HOW_MANY',
    'bao_lâu': 'HOW_LONG',
    'gì': 'WH',
    'nào': 'WH'
}

class Relation:
    def __init__(self, pred, *args):
        self.pred = pred
        self.args = args

    def __repr__(self):
        return f"({self.pred} {' '.join(map(str, self.args))})"

def extract_relations(dependencies: List[Dependency]):

    # extract useful relations based on database in input/database.txt
    relations = []

    for dep in dependencies:

        # if dep.label == 'root':
        #     relations.append(Relation('MVERB', dep.tail.word))
        
        # if dep.label in ['nsubj', 'csubj']:
        #     relations.append(Relation('SUBJ', dep.tail.word))

        # if dep.label == 'obj':
        #     relations.append(Relation('OBJ', dep.tail.word))

        if dep.tail.word == 'được_không':
            relations.append(Relation('COMMAND', dep.head.word))

        if "-Q" in dep.tail.pos:
            relations.append(Relation(QUERY_MAP[dep.tail.word], dep.head.word))

        if dep.label == 'case':
            if dep.tail.word == 'từ':
                relations.append(Relation('FROM-LOC', dep.head.word))
            if dep.tail.word == 'đến':
                relations.append(Relation('TO-LOC', dep.head.word))

        if dep.label == 'obj' and dep.head.word == 'đi':

            if dep.tail.pos == 'N-LOC' or dep.tail.word == 'tour':
                relations.append(Relation('TO-LOC', dep.tail.word))

        if dep.label == 'compound' and dep.head.word == 'tour':
            relations.append(Relation('COMP', dep.head.word, dep.tail.word))

    return relations


        

        




