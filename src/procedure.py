import re
from src.logic import LogicalFormulator

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

class ProcedureExecutor:

    DATABASE_FILE = 'input/database.txt'

    def __init__(self, proceduralizer, save=False):

        self.proceduralizer = proceduralizer
        self.database = self.import_database()
        self.save = save
    
    def proceduralize(self, logical_form):
        procedure = self.proceduralizer(logical_form)

        if self.save:
            with open(LogicalFormulator.LOGICAL_FILE, 'a', encoding='utf-8') as f:
                f.write(f'{procedure}\n\n')

        return procedure

    def proceduralize_all(self, logical_forms):

        procedures = []

        for lf in logical_forms:

            with open(LogicalFormulator.LOGICAL_FILE, 'a', encoding='utf-8') as f:
                f.write(f'---{len(procedures) + 1}---\n')

            procedures.append(self.proceduralize(lf))

        return procedures
    
    def import_database(self):
        
        db = {'TOUR': [], 'TIME': [], 'RUN-TIME': [], 'BY': []}
        with open(self.DATABASE_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            tour_pattern = re.compile(r'\(TOUR (\w+) (\w+)\)')
            time_pattern = re.compile(r'\(DTIME (\w+) (\w+) "([^"]+)"\) \(ATIME \w+ (\w+) "([^"]+)"\)')
            runtime_pattern = re.compile(r'\(RUN-TIME (\w+) (\w+) (\w+) ([\d:]+ \w+)\)')
            by_pattern = re.compile(r'\(BY (\w+) (\w+)\)')

            db['TOUR'] = tour_pattern.findall(content)
            db['TIME'] = time_pattern.findall(content)
            db['RUN-TIME'] = runtime_pattern.findall(content)
            db['BY'] = by_pattern.findall(content)

        return db

    def execute(self, procedure):
        return procedure.execute(self.database)