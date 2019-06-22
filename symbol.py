import re
import weakref


class Symbol:
    _symbols = []

    def __init__(self, name, regex = "", prods = []):
        self.name = name
        self.open_tag = "<" + name + ">"                                        # will be overwritten for literals
        self.closed_tag = re.sub("<", "</", self.open_tag)
        self.regex = regex
        self.prods = []
        self.is_terminal = False
        Symbol._symbols.append(weakref.ref(self))


    def print(self):
        print(self.name, self.is_terminal)
        # print("produkcije", len(self.prods))
        # for prod in self.prods:
        #     prod.print()



PROD_ID = 1

class Production:
    _productions = []

    @staticmethod
    def get_production(id):
        for item in Production._productions:
            if (item().id == id):
                return item()
        return None


    def __init__(self, symbols = []):
        global PROD_ID
        self.id = PROD_ID
        self.symbols = symbols
        self.regex = ""
        PROD_ID += 1
        Production._productions.append(weakref.ref(self))


    def print(self):
        for symbol in self.symbols:
            print(symbol.name, end=" ")
        print()
