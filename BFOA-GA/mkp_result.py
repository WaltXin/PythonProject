import numpy as np

worst_profit = -1


class Result(object):
    def __init__(self):
        self.best_solution = []
        self.best_profit = worst_profit

    def compute_best(self, solutions, profits):
        best_index = np.argmax(profits)
        best_profit = profits[best_index]

        if best_profit > self.best_profit:
            self.best_profit = best_profit
            self.best_solution = solutions[best_index]
