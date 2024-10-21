import random

class ContextFreeGrammar:
    """
    Context-free grammar
    """

    def __init__(self, start, rules) -> None:
        
        self.start = start
        self.rules = rules
        self.non_terminals = set(rules.keys())


    def __str__(self) -> str:

        return '\n'.join([
            f"{lhs} -> {' | '.join(
                [
                    ' '.join(rhs) 
                    for rhs in rhslist
                ]
            )}" 
            for lhs, rhslist in self.rules.items()
        ])
    

    def save(self, filename):

        with open(filename, 'w+') as f:
            f.write(str(self))


    @staticmethod
    def fromstring(s):
        """
        Parse a string representation of a CFG
        """
        start = ''
        rules = {}
        for line in s.strip().split('\n'):
            lhs, rhs = line.split(' -> ')
            if not start: 
                start = lhs
            rules[lhs] = [r.split() for r in rhs.split(' | ')]
        
        return ContextFreeGrammar(start, rules)
        

    def is_terminal(self, symbol):
        return symbol not in self.non_terminals
    

    def generate(self, max_length=10, max_samples=100, filename = 'output/samples.txt'):
        """
        Generate sentences from the grammar
        """
        # sentences = []
        count = 0
        with open(filename, 'w') as f:
            f.write('')

        # perform DFS on tree
        # node: (list of non-terminals, current sentence)
        # e.g. ([V NP], ["bạn"])
        stack = [([self.start], [])] # start with [S], []

        while stack:

            seq, sent = stack.pop(random.randint(0, len(stack) - 1)) 

            if not seq:
                with open(filename, 'a') as f:
                    f.write(' '.join(sent) + '\n')
                count += 1
                if count >= max_samples:
                    break
                continue

            if len(sent) > max_length:
                continue

            sym = seq[0]

            if self.is_terminal(sym):
                stack.append((seq[1:], sent + [sym]))
                continue

            for rhs in self.rules[sym]:
                child = (rhs + seq[1:], sent)
                stack.append(child)

    def parse(self, sentence, filename = 'output/parse-results.txt'):
        """
        Parse a sentence using the grammar with a simple top-down parser
        """
        
        with open(filename, 'a') as f:
            f.write('-----------------------------------\n')
            f.write(f"Parsing: {sentence}\n")
        stack = [([self.start], 0, [])]
        words = sentence.split()

        while stack:

            seq, i, tree = stack.pop()

            if i == len(words):
                if not seq:
                    self._dump_parse_tree(tree, filename)
                    return
                continue

            if not seq:
                continue

            sym = seq[0]

            if self.is_terminal(sym):
                if sym == words[i]:
                    stack.append((seq[1:], i + 1, tree))
                continue

            for rhs in self.rules[sym]:
                new_tree = tree + [(sym, rhs)]
                stack.append((rhs + seq[1:], i, new_tree))

            # print(stack)

        self._dump_parse_tree(None, filename)

    def parse_all(self, sentences, filename = 'output/parse-results.txt'):
        """
        Parse a list of sentences
        """
        with open(filename, 'w') as f:
            f.write('')

        for sent in sentences:
            self.parse(sent, filename)
    
    def _dump_parse_tree(self, rules, filename):

        with open(filename, 'a') as f:
            
            if not rules:
                f.write("Failed to parse the sentence!\n")
                return

            dmap = dict()
            dmap[rules[0][0]] = 0
            TAB = "\t"

            for lhs, rhs in rules:

                d = dmap[lhs]

                if self.is_terminal(rhs[0]):
                    for _ in range(d): f.write(TAB)
                    f.write(f"{lhs} {' '.join(rhs)}\n")

                else:
                    for sym in rhs: dmap[sym] = d + 1 # gotta fail if CFG is recursive
                    for _ in range(d): f.write(TAB)
                    f.write("")
                    f.write(lhs)
                    f.write("\n")



