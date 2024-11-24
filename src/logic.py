class LogicalForm:
    def __init__(self, predicate, *args):
        self.predicate = predicate
        self.var = None
        self.args = [*args]

    def add_argument(self, arg):
        self.args.append(arg)

    def __repr__(self):
        return f"({self.predicate} {' '.join(map(str, self.args))})"

class ThematicRole:
    def __init__(self, role, entity, var=None):
        self.role = role
        self.var = var
        self.entity = entity

    def __repr__(self):
        return f"[{self.role} {self.entity}]"

class Entity:
    def __init__(self, modifier, var, name):
        self.var = var
        self.name = name
        self.modifier = modifier

    def __repr__(self):
        if self.modifier in ['NAME', 'PRO']:
            return f"({self.modifier} {self.var} {self.name})"
        return f"<{self.modifier} {self.var} {self.name}>"

class LogicalFormulator:

    LOGICAL_FILE = 'output/p2-q-4.txt'

    def __init__(self, logicalizer, save=False):
        self.logicalizer = logicalizer
        self.save = save

        if save:
            with open(self.LOGICAL_FILE, 'w', encoding='utf-8') as f:
                f.write('')

    def logicalize(self, relations):
        lf = self.logicalizer(relations)

        if self.save:
            with open(self.LOGICAL_FILE, 'a', encoding='utf-8') as f:
                f.write(f'{lf}\n\n')
        
        return lf
    
    def logicalize_all(self, relation_lists):

        lfs = []

        for relations in relation_lists:

            with open(self.LOGICAL_FILE, 'a', encoding='utf-8') as f:
                f.write(f'---{len(lfs) + 1}---\n')

            lfs.append(self.logicalize(relations))

        return lfs


    
