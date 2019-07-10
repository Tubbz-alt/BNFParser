import settings
from symbol import Production

out_file = ""

def process_node(node, parse_graph, spacing = 0):
    global out_file
    symbol = node.symbol

    if symbol.is_terminal:
        print(spacing * " ", symbol.name)
        out_file.write(spacing * " " + " " + symbol.name + "\n")
    else:
        print(spacing * " ", symbol.open_tag)
        out_file.write(spacing * " " + " " + symbol.open_tag + "\n")

        if node.is_regex:
            print((spacing + settings.INDENTATION) * " ", node.match)
            out_file.write((spacing + settings.INDENTATION) * " " + " " + node.match + "\n")
        else:
            children = parse_graph.vertices[node]
            for child in children:
                process_node(child, parse_graph, spacing + settings.INDENTATION)

        print(spacing * " ", symbol.closed_tag)
        out_file.write(spacing * " " + " " + symbol.closed_tag + "\n")


def make_XML_file(parse_graph, out_filename):
    global out_file
    with open(out_filename, 'a') as out_file:
        root_node = next(iter(parse_graph.vertices))
        process_node(root_node, parse_graph)

