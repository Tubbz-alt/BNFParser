from symbol import Symbol, Production
import copy


class Prediction:
    matched_input = []
    remaining_input = []

    @staticmethod
    def process_symbol():
        Prediction.matched_input.append(Prediction.remaining_input[0])
        Prediction.remaining_input = Prediction.remaining_input[1:]

        stop_parse = False
        if not Prediction.remaining_input:
            stop_parse = True
        return stop_parse


    def __init__(self, start_symbol):
        self.analysis = []
        self.prediction = []
        self.prediction.insert(0, start_symbol)


    def replace_nonterm(self, prod):
        self.prediction.pop(0)
        i = 0
        for symbol in prod.symbols:
            self.prediction.insert(i, symbol)
            i += 1


    # update analysis management
    def move_term(self):
        self.analysis.append(self.prediction[0])
        self.prediction = self.prediction[1:]


    def not_valid(self):
        return self.prediction[0].is_terminal and Prediction.remaining_input[0] != self.prediction[0].regex


    def check_match(self):
        # only for predictions starting in terminal
        # TODO: error-checking?
        return Prediction.remaining_input[0] == self.prediction[0]


    def copy_prediction(self):
        return copy.deepcopy(self)


    def has_term_next(self):
        return self.prediction[0].is_terminal


    def has_nonterm_next(self):
        return not self.has_term_next()


    def print(self):
        # TODO: print analysis
        for symbol in self.prediction:
            print(symbol.name, end = " ")
        print()



class Parser:
    def __init__(self, input, start_symbol):
        self.predictions = []
        start_prediction = Prediction(start_symbol)
        self.predictions.append(start_prediction)
        Prediction.remaining_input = input


    def add_prediction(self, prediction):
        self.predictions.append(prediction)


    def clean_predictions(self):
        self.predictions = [prediction for prediction in self.predictions if not prediction.not_valid()]


    def fork_predictions(self):
        fork_again = False
        new_preds = []

        for prediction in self.predictions:
            # fork every production starting with nonterm
            # so every leftmost nonterm is replaces with all of its alternatives
            if prediction.has_term_next():
                new_preds.append(prediction)
            else:
                nonterm = prediction.prediction[0]
                alt_count = len(nonterm.prods)                 # no. of alt productions
                for i in range(alt_count):
                    pred_copy = prediction.copy_prediction()
                    pred_copy.replace_nonterm(nonterm.prods[i])
                    new_preds.append(pred_copy)

                    if pred_copy.has_nonterm_next():
                        fork_again = True

        self.predictions = new_preds
        return fork_again


    def print(self):
        if self.predictions:
            print("matched:", Prediction.matched_input)
            print("remaining:", Prediction.remaining_input)

            for prediction in self.predictions:
                prediction.print()
        else:
            print("no predictions")
        print("---------------------------------------------------")



    def move_predictions(self):
        for prediction in self.predictions:
            prediction.move_term()


    def parse(self):
        stop_parse = False
        while (not stop_parse):
            self.print()
            while(self.predictions and not stop_parse):
                # fork until all the predictions start with term
                # TODO: recursions
                flag = True
                while (flag):
                    flag = self.fork_predictions()

                self.print()
                print("... cleanup")
                self.clean_predictions()
                self.print()
                self.move_predictions()
                stop_parse = Prediction.process_symbol()
