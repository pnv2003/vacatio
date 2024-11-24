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

    def __repr__(self) -> str:
        return f'{self.head.word} --({self.label})-> {self.tail.word}'
    
class TransitionClassifier:

    def __init__(self, classifier):

        # use some predefined rules to classify transitions instead of a machine learning model
        self.classifier = classifier

    def classify(self, features):
        return self.classifier(features)

    def describe(self):
        return self.classifier.__doc__

class DependencyGrammar:

    GRAMMAR_FILE = 'output/p2-q-1.txt'
    PARSE_FILE = 'output/p2-q-2.txt'

    def __init__(self, tokenizer, pos_tagger, transition_classifier):
        self.tokenizer = tokenizer
        self.pos_tagger = pos_tagger
        self.transition_classifier = transition_classifier

        self.tokens = None
        self.pos_tags = None
        self.deps = None

    def save(self):

        with open(self.GRAMMAR_FILE, 'w', encoding='utf-8') as f:
            
            # summary of the grammar: tokenizer, pos_tagger, and transition_classifier
            f.write(f"""
A simple dependency grammar using an arc-eager shift-reduce parser, with the following components:

Tokenizer: {self.tokenizer}
Part-of-speech tagger: {self.pos_tagger}
Transition function: A function that takes a dictionary of features and returns a transition.

{self.extract_features.__doc__}

{self.apply_transition.__doc__}

- Rules: {self.transition_classifier.describe()}

""")

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
        self.deps = []

        if save:
            with open(self.PARSE_FILE, 'a', encoding='utf-8') as f:
                f.write('-----------------------------------\n')
                f.write(f"Parsing: {sent}\n")
                f.write('-----------------------------------\n')
                f.write(f'Tokens: {Item.dump(buffer)}\n\n')

        # shift-reduce parsing
        while buffer:
            features = self.extract_features(stack, buffer)
            transition = self.transition_classifier.classify(features)
            self.apply_transition(transition, stack, buffer, self.deps, save=save)

        if save:
            with open(self.PARSE_FILE, 'a', encoding='utf-8') as f:
                f.write('-----------------------------------\n')
                # f.write('Dependencies:\n')
                # Item.dump(dependencies)

        print("Parsing completed. Check out the variables 'tokens', 'pos_tags', and 'deps'.")
    
    def parse_all(self, sent, save=False):

        if save:
            with open(self.PARSE_FILE, 'w', encoding='utf-8') as f:
                f.write('')

        dep_lists = []

        for s in sent:
            self.parse(s, save=save)
            dep_lists.append(self.deps)

        return dep_lists
    
    def extract_features(self, stack, buffer):
        """
- Features:
    - sword: The word on top of the stack.
    - bword: The first word in the buffer.
    - spos: The part-of-speech tag of the word on top of the stack.
    - bpos: The part-of-speech tag of the first word in the buffer.
    - sindex: The index of the word on top of the stack.
    - bindex: The index of the first word in the buffer.
    - has_main_verb: Whether the stack contains a main verb.
        """
        
        features = {}

        features['deps'] = self.deps
        features['sword'] = stack[-1].word if stack else None
        features['bword'] = buffer[0].word if buffer else None
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
        """
- Transitions:

    - SHIFT: Move the first word in the buffer to the top of the stack.
    - LEFT_ARC label: Create a dependency with the first word in the buffer as the head and the word on top of the stack as the tail.
    - RIGHT_ARC label: Create a dependency with the word on top of the stack as the head and the first word in the buffer as the tail.
    - REDUCE: Remove the word on top of the stack.
        """

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
        
        if not buffer:
            # add root dependency
            head = stack.pop(0)
            tail = stack.pop(0)
            new_dep = Dependency(head, tail, 'root')
            dependencies.append(new_dep)
        
        if save:
            with open(self.PARSE_FILE, 'a', encoding='utf-8') as f:
                
                f.write("{0:<15} {1:<40} {2:<80} {3:<40}\n".format(
                        transition.split()[0],
                        str(Item.words(stack)),
                        str(Item.words(buffer)),
                        str(new_dep) if new_dep else ''
                ))