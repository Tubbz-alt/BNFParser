import re

tokens = []

# class modelling BNF tokens
class token:
    def __init__(self, name, regex = "", children = []):
        self.open_tag = name
        self.closed_tag = re.sub("<", "</", name)
        self.regex = regex
        self.children = []


# converts the right-hand-side expression of the terminal to regex
def terminal_regex(value):
    value = re.sub("\n", "", value)
    value = re.sub("\"", "", value)
    value = "(" + value + ")"
    return value


# determines if a token is a literal
def is_literal(text):
    regex = "<.*?>";                        # TODO: upgrade
    compiled = re.compile(regex)
    match = compiled.match(text)
    return match == None


# determines if a token is terminal
def is_terminal(value):
    return not "<" in value                 # TODO: upgrade


# finds and returns a token from token list by open_tag
def get_token_by_name(name):
    for token in tokens:
        if token.open_tag == name:
            return token


# splits the right-hand-side expression of non-terminal token
# creates literals (literal tokens)
# returns token names appearing on the right-hand-side (already added to token list)
def split_expr(value):
    global tokens
    names = []
    value = re.sub(" ", "", value)
    value = re.sub("\n", "", value)

    # split on "
    tokens1 = value.split("\"")
    if "" in tokens1:               # if the last symbol in a row was "
        tokens1.remove("")

    for item in tokens1:
        item = re.sub("\n", "", item)

        if is_literal(item):
#            name = "<literal>"                             # all literals can't be named <literal> - FIX
            name = item
            literal = token(name, item)                     # literal has the same name and regex; FIX name
            tokens.append(literal)                          # literals are added immediately to the token list
            names.append(name)

        else:
            tokens2 = item.split(">")

            if "" in tokens2:
                tokens2.remove("")

            new_list = [(token + ">") for token in tokens2]
            for item in new_list:
                names.append(item)

    return names


# parses .bnf file and creates synthax tree
# returns root node
def tokenize(lines):
    global tokens
    lines.reverse()                                          # starting with terminals - standard BNF symbol order assumed - UPGRADE ?

    for line in lines:
        arr = line.split(" ::= ")                            # TODO: split around ::= and remove whitespaces
        name = arr[0]
        value = arr[1]
        new_token = token(name)

        if is_terminal(value):
            new_token.regex = terminal_regex(value)
            tokens.append(new_token)                        # terminals are added immediately to the token list

        else:
            left_names = split_expr(value)
            for item in left_names:
                child = get_token_by_name(item)             # all terminals are added before non-terminals
                new_token.children.append(child)
                new_token.regex += child.regex
            tokens.append(new_token)
    tokens.reverse()
    return tokens[0]
