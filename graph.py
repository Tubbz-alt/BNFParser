from symbol import Production

NODE_ID = 1

class Node:
    def __init__(self, symbol):
        global NODE_ID
        self.symbol = symbol
        self.id = NODE_ID
        NODE_ID += 1


    @staticmethod
    def make_nodes(production):
        nodes = []
        for symbol in production.symbols:
            nodes.append(Node(symbol))
        return nodes



class Graph:
    def __init__(self, start_symbol):
        self.nodes = []
        self.vertices = {}
        self.nodes.append(start_symbol)
        self.vertices[start_symbol] = []


    # TODO: handle recursions
    def add_children(self, node, children):
        self.vertices[node] = []
        for child in children:
            self.vertices[node].append(child)


    def replace_leftmost_prod(self, nodes):
        self.nodes.pop(0)
        for node in nodes:
            if not node.symbol.is_terminal:
                self.nodes.insert(0, node)


    def print(self):
        for node in self.vertices:
            print(node.symbol.name)
            print("children: ")
            children = self.vertices[node]
            for child in children:
                print(child.symbol.name, end=" ")
            print()



def create_parse_graph(start_symbol, parse_arr, productions):
    start_node = Node(start_symbol)
    parse_graph = Graph(start_node)

    while parse_arr:
        while parse_graph.nodes[0].symbol.is_terminal:
            parse_graph.nodes.pop(0)

        parent = parse_graph.nodes[0]
        id = parse_arr.pop(0)

        production = Production.get_production(id)
        production_nodes = Node.make_nodes(production)

        parse_graph.add_children(parent, production_nodes)
        parse_graph.replace_leftmost_prod(production_nodes)

    return parse_graph
