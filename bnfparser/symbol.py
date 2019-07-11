import re


class Symbol:
    _symbols = []

    def __init__(self, name, regex = "", prods = []):
        self.name = name
        self.open_tag = "<" + name + ">"                                        # will be overwritten for literals
        self.closed_tag = re.sub("<", "</", self.open_tag)
        self.regex = regex
        self.prods = []
        self.is_terminal = False
        self.is_regex = False
        self.matched = ""
        Symbol._symbols.append(self)


    def is_productive(self, productive_symbols):
        if self.is_regex:
            return True
        for prod in self.prods:
            if prod.is_productive(productive_symbols):
                return True
        
        return False


    def print(self):
        print(self.name, self.is_terminal)
        # print("produkcije", len(self.prods))
        # for prod in self.prods:
        #     prod.print()

    

class Production:
    _productions = []       # list of all productions
    PROD_ID = 1

    @staticmethod
    def get_production(id):
        for item in Production._productions:
            if (item.id == id):
                return item
        return None


    def __init__(self, symbols = []):
        self.id = Production.PROD_ID
        self.symbols = symbols
        self.regex = ""
        Production.PROD_ID += 1
        Production._productions.append(self)
        

    def is_terminal_only(self):
        for symbol in self.symbols:
            if not symbol or not symbol.is_terminal:
                return False
        return True

    def is_productive(self, productive_symbols):
        if self.is_terminal_only():
            return True

        for symbol in self.symbols:
            # searching the list of productive symbols (so far)
            # for this symbol
            is_productive = False
            for productive_symbol in productive_symbols:
                if symbol.name == productive_symbol.name:
                    is_productive = True
            
            if not is_productive:
                return False
        
        return True


    def print(self):
        for symbol in self.symbols:
            print(symbol.name, end=" ")
        print()
