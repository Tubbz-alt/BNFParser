import re
import symbol
import parse
import bnf2graph
import format
from parsing import Parser, Prediction


# text = "111-A222 B57 111A222"                                                   # sample text
CONFIG_FILENAME = "config0.bnf"
file = open(CONFIG_FILENAME)
lines = file.readlines()

root = bnf2graph.create_prod_graph(lines)                                       # TODO: return prod_graph with method find_root


###
text = "111-A222"
parser = Parser(text, root)
parser.parse()
