import re

symbols = []

# class modelling BNF symbols
class symbol:
    def __init__(self, name, regex = "", children = []):
        self.name = name
        self.open_tag = name                                                    # will be overwritten for literals
        self.closed_tag = re.sub("<", "</", name)
        self.regex = regex
        self.children = []


# converts terminal expression to regex
def create_terminal_regex(value):
    value = re.sub("\n", "", value)
    value = re.sub("\"", "", value)
    value = "(" + value + ")"
    return value


# determines if symbol is literal
def is_literal(text):
    regex = "<.*?>";                                                            # TODO: upgrade in case of literal containing "<" or ">"
    compiled = re.compile(regex)
    match = compiled.match(text)
    return match == None


# determines if a symbol is terminal
def is_terminal_expr(value):
    return not "<" in value                 # TODO: upgrade


# finds symbol by name from symbol list
def get_symbol(name):
    for symbol in symbols:
        if symbol.name == name:
            return symbol


# creates literal
def create_literal(item):
    literal = symbol(item, item)
    literal.open_tag = "<literal>"
    literal.closed_tag = "</literal>"

    return literal


def split_expr(expr, separator):
    arr = expr.split(separator)
    if "" in arr:
        arr.remove("")

    return arr


# splits non-terminal expression
# returns symbol names appearing in expression
def expr_symbol_names(expr):
    global symbols
    names = []

    expr = re.sub(" ", "", expr)
    expr = re.sub("\n", "", expr)

    tokens1 = split_expr(expr, "\"")                                            # attempts to extract literals

    for item in tokens1:
        item = re.sub("\n", "", item)

        if is_literal(item):
            literal = create_literal(item)
            symbols.append(literal)                                             # literals added immediately to the symbol list
            names.append(literal.name)

        else:
            tokens2 = split_expr(item, ">")                                     # complex token; splits further and extract non-literals
            symbol_names = [(name + ">") for name in tokens2]
            for name in symbol_names:
                names.append(name)

    return names


# sorts rules from non-terminals to terminals
def sort_rules(lines):
    lines.reverse()                                                             # assumes standard BNF rule order (from terminals to non-terminals)


# splits rule elements
def split_line(line):
    arr = line.split(" ::= ")
    return [arr[0], arr[1]]


# parses .bnf file and creates synthax tree
# returns root node
def tokenize(lines):
    global symbols

    sort_rules(lines)

    for line in lines:
        [name, expr] = split_line(line)
        new_symbol = symbol(name)

        if is_terminal_expr(expr):
            new_symbol.regex = create_terminal_regex(expr)
            symbols.append(new_symbol)                                          # terminals added immediately to the symbol list

        else:
            children_names = expr_symbol_names(expr)
            for child_name in children_names:
                child = get_symbol(child_name)                                  # both terminals and children of non-terminal added before the non-terminal; TODO: RECURSIVE DEFINITION
                new_symbol.children.append(child)
                new_symbol.regex += child.regex
            symbols.append(new_symbol)


    return symbols[len(symbols) - 1]                         # returs root symbol
