import copy
import re
from symbol import Symbol, Production


class Prediction:
    input = []

    def __init__(self, start_symbol):
        self.pos = 0
        self.analysis = []
        self.prediction = []
        self.prediction.insert(0, start_symbol)


    def replace_nonterm(self, prod):
        self.prediction.pop(0)
        i = 0
        for symbol in prod.symbols:
            self.prediction.insert(i, symbol)
            i += 1


    def next_input_symbol(self, end = 1):                       # end may differ for shifting regex pred symbols
        self.prediction = self.prediction[1:]
        self.pos += end

        no_input = self.pos == len(Prediction.input)
        return no_input


    # if the first symbol is terminal, discards if it doesn't match the current input symbol
    # if the first symbol is regex, discards if it doesn't match any no of first input symbols
    def not_valid(self):
        if self.prediction[0].is_terminal:
            return Prediction.input[self.pos] != self.prediction[0].regex
        elif self.prediction[0].is_regex:
            print("testing regex", self.prediction[0].regex)
            print("input:", Prediction.input[self.pos:])
            symbol = self.prediction[0]
            compiled = re.compile(symbol.regex)
            return not re.match(compiled, Prediction.input[self.pos:])


    def copy_prediction(self):
        return copy.deepcopy(self)


    def has_term_next(self):
        return self.prediction[0].is_terminal


    def has_nonterm_next(self):
        return not self.has_term_next() and not self.has_regex_next()


    def has_regex_next(self):
        return self.prediction[0].is_regex


    def is_empty(self):
        return not self.prediction


    def print(self):
        for symbol in self.prediction:
            print(symbol.name, end=" ")
        print()



class Parser:
    # temp array for storing forked predictions
    _new_predictions = []

    def __init__(self, input, start_symbol):
        self.predictions = []
        Prediction.input = input
        start_prediction = Prediction(start_symbol)
        self.predictions.append(start_prediction)


    def clean_predictions(self):
        self.predictions = [pred for pred in self.predictions if pred.has_nonterm_next() or not pred.not_valid()]
        no_predictions = False if self.predictions else True
        return no_predictions


    def fork_prediction(self, prediction):
        if prediction.has_term_next():
            Parser._new_predictions.append(prediction)
        elif prediction.has_regex_next():
            Parser._new_predictions.append(prediction)
        else:
            nonterm = prediction.prediction[0]
            alt_count = len(nonterm.prods)
            for i in range(alt_count):
                pred_copy = prediction.copy_prediction()
                pred_copy.replace_nonterm(nonterm.prods[i])
                pred_copy.analysis.append(nonterm.prods[i].id)
                Parser._new_predictions.append(pred_copy)


    def shift_predictions(self):
        for prediction in self.predictions:
            # prediction[0] is a matched terminal or regex
            if prediction.has_term_next():
                no_input = prediction.next_input_symbol()
                if no_input:
                    successful_pred = prediction
                    return successful_pred
            # uvijek grabi najveci match, bez obzira na to sta dolazi poslije

            elif prediction.has_regex_next():                                   # matched SOMETHING
                compiled = re.compile(prediction.prediction[0].regex)
                match = re.match(compiled, Prediction.input[prediction.pos:])
                end = match.end()
                no_input = prediction.next_input_symbol(end)
                prediction.analysis.append({"match": match.group(0)})

                if no_input and not prediction.prediction: # nema simbola poslije regex-a
                    successful_pred = prediction
                    return successful_pred


    def remove_empty_predictions(self):
        self.predictions = [pred for pred in self.predictions if pred.prediction]


    def print(self):
        if self.predictions:
            for item in self.predictions:
                item.print()
        else:
            print("no predictions")
        print("---------------------------------------------------")


    def parse(self):
        stop_parse = False

        # stops when there are no predictions left
        # or when a successful match is found
        while(self.predictions and not stop_parse):
            for prediction in self.predictions:
                # forks predictions starting with nonterm
                self.fork_prediction(prediction)

            # swap current predictions arr with forked
            self.predictions = Parser._new_predictions.copy()
            Parser._new_predictions.clear()

            print("-- forked predictions")
            self.print()

            # removes predictions with nonmatching terminal
            no_predictions = self.clean_predictions()
            print("-- cleaned predictions")
            self.print()
            if no_predictions:                                                  # <=> self.predictions is empty
                # print("NO PREDICTIONS LEFT")
                print("MATCH NOT FOUND")
            else:
                successful_pred = self.shift_predictions()
                print("-- shifted predictions")
                self.print()
                self.remove_empty_predictions()                                 # if there are still input symbols but no nonterms in prediction
                print("-- removed empty predictions")
                self.print()
                if successful_pred:
                    print("PROCESSING DONE")
                    print("MATCH FOUND")
                    return successful_pred.analysis                             # linearized parse tree
                elif not self.predictions:
                    print("NO PREDICTIONS LEFT")
                    print("MATCH NOT FOUND")
                    stop_parse = True
