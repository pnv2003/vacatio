class Relation:
    def __init__(self, pred, *args):
        self.pred = pred
        self.args = args

    def __repr__(self):
        return f"({self.pred} {' '.join(map(str, self.args))})"