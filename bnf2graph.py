import re, copy
from symbol import Symbol, Production

nonterms = []

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
    for symbol in nonterms:
        if symbol.name == name:
            return symbol


def split_expr(expr, separator):
    return expr.split(separator)


# tokenizes prod rhs
def split_prod(expr):
    global nonterms
    symbols = []

    expr = re.sub(" ", "", expr)
    expr = re.sub("\n", "", expr)                                               # in case terminal is at the end

    tokens1 = split_expr(expr, "\"")                                            # attempts to extract terminals
    # print(tokens1)

    for item in tokens1:
        item = re.sub("\n", "", item)
        # print(item)

        # split on " isolates terminals
        if is_terminal(item):
            terminal = create_terminal(item)
            nonterms.append(terminal)                                           # terminals added immediately to the symbol list
            symbols.append(terminal)
        else:
            tokens2 = split_expr(item, ">")                                     # complex token; splits further and extracts nonterms
            if "" in tokens2:
                tokens2.remove("")
            # print("tokens2", tokens2)
            symbol_names = [(name + ">") for name in tokens2]
            # print(symbol_names)
            for name in symbol_names:
                symbols.append(get_symbol(name[1:-1]))

    return symbols


# converts prod rhs to list of alternatives
def make_prods(expr):
    prods = []

    alts = split_prods(expr)
    for alt in alts:
        # print(alt)
        symbols = split_prod(alt)
        # print(symbols)
        production = Production(symbols)
        prods.append(production)

    return prods


def copy_dict(dict):
    return copy.deepcopy(dict)

# populates nonterm symbols list
def create_nonterms(lines):
    global nonterms

    rules = make_rules(lines)
    rules_cpy = copy_dict(rules)

    for rule in rules:
        name = rule[1:-1]
        symbol = Symbol(name)
        expr = rules[rule]

        if (not has_nonterms(expr)):
            symbol.regex = term_regex(expr)
            del rules_cpy[rule]
        nonterms.append(symbol)

    for rule in rules_cpy:
        name = rule[1:-1]
        symbol = get_symbol(name)
        prods = make_prods(rules_cpy[rule])
        symbol.prods = prods


# finds the start symbol
def find_root():
    pass


# updates symbol regexes
def update_regex():
    for symbol in nonterms:
        symbol.update_regex()


# entry point
def create_prod_graph(rules):
    create_nonterms(rules)
    #
    # symbol = get_symbol("reg_oznaka")
    # print(len(symbol.prods))
    # for prod in symbol.prods:
    #     for item in prod.symbols:
    #         if item:
    #             print(item.open_tag)
    #         else:
    #             print("NEMA")
    update_regex()
    return nonterms[0]
