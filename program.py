import re

import symbol
import parse
import bnf
import format
import graph
import settings
from symbol import Production
from parse import Parser, Prediction


def copy_init_config():
    with open(settings.CONFIG_FILENAME) as in_file, open(settings.EXT_CONFIG_FILENAME, 'w') as out_file:
        out_file.write("")
        lines = in_file.readlines()
        for line in lines:
            out_file.write(line)


copy_init_config()
start_symbol = bnf.create_prod_graph()

###
text = "051501302"
parser = Parser(text, start_symbol)
parse_arr = parser.parse()

if parse_arr:
    parse_graph = graph.create_parse_graph(start_symbol, parse_arr, Production._productions)
    format.make_XML_file(parse_graph)
