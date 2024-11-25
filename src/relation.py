class Relation:
    def __init__(self, pred, *args):
        self.pred = pred
        self.var = None
        self.args = [*args]

    def make_variable(self, var):
        self.var = var

    def __repr__(self):
        return f"({self.pred} {self.var} {' '.join(map(str, self.args))})"
