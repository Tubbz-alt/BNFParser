import re, copy
from symbol import Symbol, Production

symbols = []

# checks if prod rhs contains nonterm symbols
def has_nonterms(expr):
    return "<" in expr                                                          # upgrade


# converts terminals-only prod rhs to regex
def term_regex(expr):
    regex = re.sub("\n", "", expr)
    regex = re.sub("\"", "", regex)
    regex = "(" + regex + ")"
    return regex


# converts string rules to dict
def make_rules(lines):
    rules = {}
    for line in lines:
        [left, right] = line.split(" ::= ")
        rules[left] = right
    return rules


# splits prod rhs on |
def split_prods(expr):
    return expr.split("|")


# checks if prod rhs element is terminal
def is_terminal(expr):
    regex = "<.*>"
    compiled = re.compile(regex)
    match = compiled.search(expr)
    return not match


# creates terminal symbol
def create_terminal(expr):
    terminal = Symbol(expr, expr)
    terminal.open_tag = "<terminal>"
    terminal.closed_tag = "</terminal>"
    return terminal


# finds symbol by name from symbol list
def get_symbol(name):
    for symbol in symbols:
        if symbol.name == name:
            return symbol


def split_expr(expr, separator):
    return expr.split(separator)


# tokenizes prod rhs
def split_prod(expr):
    global symbols
    list = []

    expr = re.sub(" ", "", expr)
    expr = re.sub("\n", "", expr)                                               # in case terminal is at the end

    tokens1 = split_expr(expr, "\"")                                            # attempts to extract terminals

    for item in tokens1:
        item = re.sub("\n", "", item)

        # split on " isolates terminals
        if is_terminal(item):
            terminal = create_terminal(item)
            symbols.append(terminal)                                           # terminals added immediately to the symbol list
            list.append(terminal)
        else:
            tokens2 = split_expr(item, ">")                                     # complex token; splits further and extracts nonterms
            if "" in tokens2:
                tokens2.remove("")
            symbol_names = [(name + ">") for name in tokens2]
            for name in symbol_names:
                list.append(get_symbol(name[1:-1]))

    return list


# converts prod rhs to list of alternatives
def make_prods(expr):
    prods = []

    alts = split_prods(expr)
    for alt in alts:
        symbols = split_prod(alt)
        production = Production(symbols)
        prods.append(production)

    return prods


def copy_obj(obj):
    return copy.deepcopy(obj)


# populates symbols list
def create_symbols(lines):
    global symbols

    rules = make_rules(lines)
    rules_cpy = copy_obj(rules)

    for rule in rules:
        name = rule[1:-1]
        symbol = Symbol(name)
        expr = rules[rule]

        if (not has_nonterms(expr)):
            symbol.regex = term_regex(expr)
            del rules_cpy[rule]
        symbols.append(symbol)

    for rule in rules_cpy:
        name = rule[1:-1]
        symbol = get_symbol(name)
        prods = make_prods(rules_cpy[rule])
        symbol.prods = prods


# TODO: upgrade
def has_symbol(list, symbol):
    for item in list:
        if item.name == symbol.name:
            return True
    return False


# finds the start symbol
# start symbol can never appear on the prod rhs
# TODO: can appear on its own rhs
# test by swaping rules in .bnf file
def find_root():
    symbol_names = [symbol.name for symbol in symbols]

    for symbol in symbols:
        for prod in symbol.prods:
            for element in prod.symbols:
                if element != symbol and element.name in symbol_names:           # start symbol can self-reference
                        symbol_names.remove(element.name)

    return get_symbol(symbol_names[0])                                          # TODO: check if there is more than 1 start symbol


# updates symbol regexes
def update_regex():
    for symbol in symbols:
        symbol.update_regex()


# entry point
def create_prod_graph(rules):
    create_symbols(rules)
    update_regex()
    return find_root()
