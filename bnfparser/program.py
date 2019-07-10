import re

import symbol
import parse
import bnf
import format
import graph
import settings
from symbol import Production
from parse import Parser, Prediction


### entry point

# copy initial bnf in new file
settings.copy_init_config()

# find root symbol
start_symbol = bnf.create_prod_graph()

# text to parse (TODO: files)
text = "051-A501"

# parse
parser = Parser(text, start_symbol)
parse_arr = parser.parse()

if parse_arr:
    parse_graph = graph.create_parse_graph(start_symbol, parse_arr, Production._productions)
    format.make_XML_file(parse_graph)