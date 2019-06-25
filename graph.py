from symbol import Production


class Node:
    NODE_ID = 1

    def __init__(self, symbol, is_regex = False, match = ""):
        self.symbol = symbol
        self.id = Node.NODE_ID
        self.is_regex = is_regex
        self.match = match
        Node.NODE_ID += 1


    @staticmethod
    def make_nodes(production):
        _nodes = []
        for symbol in production.symbols:
            _nodes.append(Node(symbol))
        return _nodes



class Graph:
    def __init__(self, start_symbol):
        self._nodes = []
        self.vertices = {}
        self._nodes.append(start_symbol)
        self.vertices[start_symbol] = []


    # TODO: handle recursions
    def add_children(self, node, children):
        self.vertices[node] = []
        for child in children:
            self.vertices[node].append(child)


    def replace_leftmost_prod(self, nodes):
        self._nodes.pop(0)
        i = 0
        for node in nodes:
            if not node.symbol.is_terminal:
                self._nodes.insert(i, node)
                i += 1
        

    def print(self):
        for node in self.vertices:
            print(node.symbol.name)
            print("children: ")
            children = self.vertices[node]
            for child in children:
                print(child.symbol.name, end=" ")
            print()


# pops the first regex match from parse_arr
def find_match(parse_arr):
    for item in parse_arr:
        if type(item) is dict:
            parse_arr.remove(item)
            return item["match"]



def create_parse_graph(start_symbol, parse_arr, productions):
    start_node = Node(start_symbol)
    parse_graph = Graph(start_node)

    while parse_arr:
        parent = parse_graph._nodes[0]
        id = parse_arr.pop(0)
        production = Production.get_production(id)
        production_nodes = Node.make_nodes(production)
        for node in production_nodes:
            if node.symbol.is_regex:
                node.is_regex = True
                node.match = find_match(parse_arr)

        parse_graph.add_children(parent, production_nodes)

        # removing regex nodes from the list
        production_nodes = [node for node in production_nodes if not node.symbol.is_regex]
        parse_graph.replace_leftmost_prod(production_nodes)


    return parse_graph
