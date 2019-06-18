import re


# class modelling nontermminal symbols
class Symbol:
    def __init__(self, name, regex = "", prods = []):
        self.name = name
        self.terminal = False
        self.open_tag = "<" + name + ">"                                        # will be overwritten for literals
        self.closed_tag = re.sub("<", "</", self.open_tag)
        self.regex = regex
        self.prods = []                                                         # possible productions


    def update_regex(self):
        if (self.regex == ""):
            if len(self.prods) == 1 and not self.terminal:                      # len(self.prods) == 0 for nonterms mapping to terms only
                prod = self.prods[0]
                prod.update_regex()
                self.regex = prod.regex
            elif len(self.prods) > 1:
                self.regex += "("
                for prod in self.prods:
                    if prod.regex == "":
                        prod.update_regex()
                    self.regex += prod.regex + "|"

                self.regex = self.regex[0:-1] + ")"                             # eliminating the last |


class Production:
    def __init__(self, symbols = []):
        self.symbols = symbols
        self.regex = ""


    def update_regex(self):
        if (self.regex == ""):
            self.regex += "("
            for symbol in self.symbols:
                if symbol.regex == "":
                    symbol.update_regex()
                self.regex += symbol.regex
            self.regex += ")"


    def print_prod(self):
        pass
