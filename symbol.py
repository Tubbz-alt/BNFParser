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





class Production:
    _productions = []
    PROD_ID = 1

    @staticmethod
    def get_production(id):
        for item in Production._productions:
            if (item().id == id):
                return item()
        return None


    def __init__(self, symbols = []):
        self.id = Production.PROD_ID
        self.symbols = symbols
        self.regex = ""
        Production.PROD_ID += 1
        Production._productions.append(weakref.ref(self))


    def print(self):
        for symbol in self.symbols:
            print(symbol.name, end=" ")
        print()
