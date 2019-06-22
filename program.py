import re
import symbol
import parse
import bnf2graph
import format
import graph
from symbol import Production
from parsing import Parser, Prediction



CONFIG_FILENAME = "config0.bnf"
file = open(CONFIG_FILENAME)
lines = file.readlines()

start_symbol = bnf2graph.create_prod_graph(lines)                                    


###
text = "111-A234"
parser = Parser(text, start_symbol)
parse_arr = parser.parse()

if parse_arr:
    parse_graph = graph.create_parse_graph(start_symbol, parse_arr, Production._productions)
    parse_graph.print()
