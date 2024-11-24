class Tokenizer:

    # use an additional token map for multi-word tokens (e.g. New York)
    def __init__(self, token_map):
        self.token_map = token_map

    def tokenize(self, text):

        tokens = []
        if text[-1] in ['.', '?', '!']:
            text = text[:-1] + ' ' + text[-1]
        words = text.split()

        phrase_maxlen = max(map(len, self.token_map.keys()))

        i = 0
        while i < len(words):
            # check for multi-word tokens
            for j in range(i + phrase_maxlen, i, -1):
                phrase = ' '.join(words[i:j])
                if phrase in self.token_map.keys():
                    tokens.append(self.token_map[phrase])
                    i = j - 1
                    break
            else:
                tokens.append(words[i])
            i += 1

        return tokens
    
    def __str__(self):
        return f"""
A simple tokenizer based on space separation and a token map for multi-word tokens:

{self.token_map}
"""
    
class POSTagger:

    # use a predefined pos dictionary
    def __init__(self, pos_dict):
        self.pos_dict = pos_dict

    def tag(self, tokens):

        pos_tags = []

        # iterate over the tokens
        for token in tokens:
            # check if the token is in the pos dictionary
            if token in self.pos_dict:
                # add the pos tag
                pos_tags.append(self.pos_dict[token])
            else:
                # add a default pos tag
                pos_tags.append('UNK')
                print(f'Warning: Unknown token "{token}"')

        return pos_tags
    
    def __str__(self):
        return f"""
A simple part-of-speech tagger based on a predefined pos dictionary:

{self.pos_dict}
"""
    
class VariableManager:

    def __init__(self):
        self.variables = {}

    def set(self, name, value):

        # name: tour, time -> key: t1, t2, ...
        
        key = name.lower()[0] + '1'

        while key in self.variables:
            if self.variables[key] == value:
                break
            key = key[:-1] + str(int(key[-1]) + 1)

        self.variables[key] = value
        
        return key

    def get(self, name):
        return self.variables.get(name, None)