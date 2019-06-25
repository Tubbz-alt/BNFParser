import re

import symbol
import parse
import bnf
import format
import graph
import settings
from symbol import Production
from parse import Parser, Prediction



file = open(settings.CONFIG_FILENAME)
lines = file.readlines()

start_symbol = bnf.create_prod_graph(lines)


###
text = "AAEAA"
parser = Parser(text, start_symbol)
parse_arr = parser.parse()

if parse_arr:
    parse_graph = graph.create_parse_graph(start_symbol, parse_arr, Production._productions)
    format.make_XML_file(parse_graph)
