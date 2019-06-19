ID = 1

class Token:
    def __init__(self, symbol, match):
        global ID
        ID += 1
        self.id = ID
        self.symbol = symbol
        self.match = match
