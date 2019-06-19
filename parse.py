import re
import symbol
from token import Token


tokens = []
parse_tree = {}

INDENTATION = 3


def find_token(token, parse_tree):
    for key in parse_tree:
        if key.id == token.id:
            return token


def make_root_token(root, text):
    global parse_tree
    compiled = re.compile(root.regex)
    match = compiled.match(text)
    root_token = Token(root, match.group(0))
    return root_token


# creates parse tree
def parse(token, text, pos = 0):
    global parse_tree

    if not parse_tree:                                          # root symbol was param
        token = make_root_token(token, text)

    if not token.symbol.prods:
        compiled = re.compile(token.symbol.regex)
        match = compiled.search(text, pos)
        parse_tree[token] = []
    else:
        for prod in token.symbol.prods:
            compiled = re.compile(prod.regex)
            match = compiled.search(text, pos)
            if match:
                parse_tree[token] = []
                for symbol in prod.symbols:
                    compiled = re.compile(symbol.regex)
                    match = compiled.search(text, pos)
                    child_token = Token(symbol, match.group(0))
                    pos = match.end()
                    parse_tree[token].append(child_token)
                    parse(child_token, match.group(0))

    return parse_tree
