class Procedure:
    """
    Represents a procedural semantic form that interacts with the database.

    - SELECT <query> FROM <data> WHERE <criteria>: select items from the database that match the criteria
    - FILTER <data> BY <criteria>: filter items from the database that match the criteria
    - data: TOUR | DTIME | ATIME | RUN-TIME | BY
    """

    def __init__(self, action):
        self.action = action
        self.next = None # next procedure in the sequence

    def execute(self, database):
        raise NotImplementedError
    
class SelectProcedure(Procedure):

    def __init__(self, query, data, criteria):
        super().__init__('SELECT')
        self.query = query
        self.data = data
        self.criteria = criteria

    def execute(self, database):
        
        records = database[self.data]
        result = []

        for rec in records:
            
            if all([
                r == c or c is None
                for r, c in zip(rec, self.criteria)
            ]):
                if type(self.query) in [list, tuple]:
                    result.append([rec[q - 1] for q in self.query])
                else:
                    result.append(rec[self.query - 1])

        return result

    def __repr__(self):
        return f"SELECT {self.query} FROM {self.data} WHERE {self.criteria}"
    
class FilterProcedure(Procedure):

    def __init__(self, data, criteria):
        super().__init__('FILTER')
        self.data = data
        self.criteria = criteria

    def execute(self, database):
        
        records = database[self.data]
        result = []

        for rec in records:
            
            if all([
                r == c or c is None
                for r, c in zip(rec, self.criteria)
            ]):
                result.append(rec)

        return result

    def __repr__(self):
        return f"FILTER {self.data} BY {self.criteria}"
