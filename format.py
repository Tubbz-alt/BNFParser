import settings
from symbol import Production

def process_node(node, parse_graph, spacing = 0):
    symbol = node.symbol

    if symbol.is_terminal:
        print(spacing * " ", symbol.name)
    else:
        print(spacing * " ", symbol.open_tag)

        if node.is_regex:
            print((spacing + settings.INDENTATION) * " ", node.match)
        else:
            children = parse_graph.vertices[node]
            for child in children:
                process_node(child, parse_graph, spacing + settings.INDENTATION)

        print(spacing * " ", symbol.closed_tag)



def make_XML_file(parse_graph):
    root_node = next(iter(parse_graph.vertices))
    process_node(root_node, parse_graph)
