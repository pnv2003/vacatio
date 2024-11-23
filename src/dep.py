class Item:

    def __init__(self, index, word, pos):
        self.index = index
        self.word = word
        self.pos = pos

    def __str__(self) -> str:
        return f'{self.word} ({self.pos})'
    
    @staticmethod
    def dump(items):
        return ' '.join([str(item) for item in items])

    @staticmethod
    def words(items):
        return [item.word for item in items]

class Dependency:
    
    def __init__(self, head, tail, label):
        self.head = head
        self.tail = tail 
        self.label = label

    def __str__(self) -> str:
        return f'{self.head.word} --({self.label})-> {self.tail.word}'

class DependencyGrammar:

    GRAMMAR_FILE = 'output/p2-q-1.txt'
    PARSE_FILE = 'output/p2-q-2.txt'

    def __init__(self, tokenizer, pos_tagger, get_transition):
        self.tokenizer = tokenizer
        self.pos_tagger = pos_tagger
        self.get_transition = get_transition

        self.tokens = None
        self.pos_tags = None

    def parse(self, sent, save=False):
    
        # tokenize
        self.tokens = self.tokenizer.tokenize(sent)

        # part-of-speech tagging
        self.pos_tags = self.pos_tagger.tag(self.tokens)

        # initialize the parser
        stack = []
        buffer = [Item(0, 'ROOT', 'ROOT')] + [
            Item(index, word, pos)
            for index, (word, pos) in enumerate(zip(self.tokens, self.pos_tags))
        ]
        dependencies = []

        if save:
            with open(self.PARSE_FILE, 'a', encoding='utf-8') as f:
                f.write('-----------------------------------\n')
                f.write(f"Parsing: {sent}\n")
                f.write('-----------------------------------\n')
                f.write(f'Tokens: {Item.dump(buffer)}\n\n')

        # shift-reduce parsing
        while buffer:
            features = self.extract_features(stack, buffer)
            transition = self.get_transition(features, dependencies)
            self.apply_transition(transition, stack, buffer, dependencies, save=save)

        if save:
            with open(self.PARSE_FILE, 'a', encoding='utf-8') as f:
                f.write('-----------------------------------\n')
                # f.write('Dependencies:\n')
                # Item.dump(dependencies)

        return dependencies
    
    def parse_all(self, sent):
        with open(self.PARSE_FILE, 'w', encoding='utf-8') as f:
            f.write('')

        for s in sent:
            self.parse(s, save=True)
    
    def extract_features(self, stack, buffer):
        
        features = {}

        features['spos'] = stack[-1].pos if stack else None
        features['bpos'] = buffer[0].pos if buffer else None
        features['sindex'] = stack[-1].index if stack else None
        features['bindex'] = buffer[0].index if buffer else None
        features['has_main_verb'] = any([
            item.pos == 'V'
            for item in stack[:-1]
        ])

        return features

    def apply_transition(self, transition, stack, buffer, dependencies, save=False):

        new_dep = None

        if transition == 'SHIFT':
            stack.append(buffer.pop(0))
        elif transition.startswith('LEFT_ARC'):
            head = buffer[0]
            tail = stack.pop(-1)
            label = transition.split()[1]
            new_dep = Dependency(head, tail, label)
            dependencies.append(new_dep)
        elif transition.startswith('RIGHT_ARC'):
            head = stack[-1]
            tail = buffer.pop(0)
            label = transition.split()[1]
            new_dep = Dependency(head, tail, label)
            dependencies.append(new_dep)
            stack.append(tail)
        elif transition == 'REDUCE':
            if not stack:
                Item.dump(buffer)
            stack.pop(-1)
        else:
            raise ValueError(f'Invalid transition: {transition}')
        
        if save:
            with open(self.PARSE_FILE, 'a', encoding='utf-8') as f:
                
                f.write("{0:<15} {1:<40} {2:<80} {3:<40}\n".format(
                        transition.split()[0],
                        str(Item.words(stack)),
                        str(Item.words(buffer)),
                        str(new_dep) if new_dep else ''
                ))