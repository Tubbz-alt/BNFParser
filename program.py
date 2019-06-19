import re
import symbol
import parse
import bnf2graph
import format


# text = "111-A222 B57 111A222"                                                   # sample text
CONFIG_FILENAME = "config0.bnf"
file = open(CONFIG_FILENAME)
lines = file.readlines()

root = bnf2graph.create_prod_graph(lines)                                       # TODO: return prod_graph with method find_root

# tekst ide u input parse-a
text = "AAA"
parse_tree = parse.parse(root, text)
format.print_parse_tree(parse_tree)
