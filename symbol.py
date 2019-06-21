import re


class Symbol:
    def __init__(self, name, regex = "", prods = []):
        self.name = name
        self.open_tag = "<" + name + ">"                                        # will be overwritten for literals
        self.closed_tag = re.sub("<", "</", self.open_tag)
        self.regex = regex
        self.prods = []
        self.is_terminal = False


    def print(self):
        print(self.name, self.is_terminal)
        print("produkcije", len(self.prods))
        for prod in self.prods:
            prod.print()



class Production:
    def __init__(self, symbols = []):
        self.symbols = symbols
        self.regex = ""


    def print(self):
        for symbol in self.symbols:
            print(symbol.name, end=" ")
        print()
