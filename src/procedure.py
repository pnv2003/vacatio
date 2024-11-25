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
        
        var = {}
        q = None
        if type(self.query) is int:
            var[self.query] = '?x'
            q = '?x'
        elif type(self.query) in [list, tuple]:
            var[self.query[0]] = '?x'
            var[self.query[1]] = '?y'
            q = '?x ?y'
        #TODO: add more cases for query length

        pattern = None
        pattern = self.criteria.copy()
        for i, v in var.items():
            pattern[i - 1] = v
        c = None
        if self.data == 'TIME':
            # special case: (DTIME * * *) (ATIME * * *)

            c = (
                '(DTIME' + 
                ' ' + (pattern[0] if pattern[0] else '*') +
                ' ' + (pattern[1] if pattern[1] else '*') +
                ' ' + (pattern[2] if pattern[2] else '*') +
                ') (ATIME' +
                ' ' + (pattern[0] if pattern[0] else '*') +
                ' ' + (pattern[3] if pattern[3] else '*') +
                ' ' + (pattern[4] if pattern[4] else '*') +
                ')'
            )

        else:
            c = (
                f'({self.data} ' +
                ' '.join(
                    [str(x) if x else '*' for x in pattern]
                ) + ')'
            )

        return f'SELECT {q} {c}'        
    
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
        
        c = None

        if self.data == 'TIME':

            c = (
                '(DTIME' + 
                ' ' + (self.criteria[0] if self.criteria[0] else '*') +
                ' ' + (self.criteria[1] if self.criteria[1] else '*') +
                ' ' + (self.criteria[2] if self.criteria[2] else '*') +
                ') (ATIME' +
                ' ' + (self.criteria[0] if self.criteria[0] else '*') +
                ' ' + (self.criteria[3] if self.criteria[3] else '*') +
                ' ' + (self.criteria[4] if self.criteria[4] else '*') +
                ')'
            )

        else:

            c = (
                f'({self.data} ' +
                ' '.join(
                    [str(x) if x else '*' for x in self.criteria]
                ) + ')'
            )

        return f'FILTER {c}'
