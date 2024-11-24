class Relation:
    def __init__(self, pred, *args):
        self.pred = pred
        self.var = None
        self.args = [*args]

    def make_variable(self, var):
        self.var = var

    def __repr__(self):
        return f"({self.pred} {self.var} {' '.join(map(str, self.args))})"
    
class RelationExtractor:

    RELATION_FILE = 'output/p2-q-3.txt'

    def __init__(self, extractor, save=False):
        self.extractor = extractor
        self.save = save

        if save:
            with open(self.RELATION_FILE, 'w', encoding='utf-8') as f:
                f.write('')

    def extract(self, dependencies):
        relations = self.extractor(dependencies)

        if self.save:
            with open(self.RELATION_FILE, 'a', encoding='utf-8') as f:
                for relation in relations:
                    f.write(f'{relation}\n')
                f.write('\n')

        return relations
    
    def extract_all(self, deplists):

        relation_lists = []

        for deps in deplists:

            with open(self.RELATION_FILE, 'a', encoding='utf-8') as f:
                f.write(f'---{len(relation_lists) + 1}---\n')
            relation_lists.append(self.extract(deps))

        return relation_lists

    