import re

import symbol
import parse
import bnf
import format
import graph
from symbol import Production
from parse import Parser, Prediction



CONFIG_FILENAME = "config.bnf"
file = open(CONFIG_FILENAME)
lines = file.readlines()

start_symbol = bnf.create_prod_graph(lines)


###
text = "111-A234"
parser = Parser(text, start_symbol)
parse_arr = parser.parse()

if parse_arr:
    parse_graph = graph.create_parse_graph(start_symbol, parse_arr, Production._productions)
    format.make_XML_file(parse_graph)
