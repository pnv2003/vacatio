class LogicalForm:
    def __init__(self, predicate, *args):
        self.predicate = predicate
        self.var = None
        self.args = [*args]

    def add_argument(self, arg):
        self.args.append(arg)

    def __repr__(self):
        return f"({self.predicate} {self.var + ' ' if self.var else ''}{' '.join(map(str, self.args))})"

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
