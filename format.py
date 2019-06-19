import parse

INDENTATION = 3

def print_token(token, parse_tree, spacing = 0):
    print(spacing * " ", token.symbol.open_tag)

    token = parse.find_token(token, parse_tree)
    if not parse_tree[token]:
        print(spacing * " ", token.match)
    else:
        for child in parse_tree[token]:
            print_token(child, parse_tree, spacing + INDENTATION)

    print(spacing * " ", token.symbol.closed_tag)


def print_parse_tree(parse_tree):
    root_token = next(iter(parse_tree))
    print_token(root_token, parse_tree)
