import numpy as np


class WorkUnit(object):
    def __init__(self, solutions, profits):
        self.solutions = solutions
        self.profits = profits

    def get_best(self, x):
        self.sort()
        return self.solutions[:x], self.profits[:x]

    def replace_worst(self, new_solutions, new_profits):
        solutions = np.concatenate([self.solutions, new_solutions])
        profits = np.concatenate([self.profits, new_profits])

        profits_with_index = [(x, i) for i, x in enumerate(profits)]
        profits_with_index.sort(reverse=True)
        profits_with_index = profits_with_index[:len(self.solutions)]

        self.solutions = np.array([solutions[i] for x, i in profits_with_index])
        self.profits = np.array([profits[i] for x, i in profits_with_index])

    def sort(self):
        profits_with_index = [(x, i) for i, x in enumerate(self.profits)]
        profits_with_index.sort(reverse=True)

        self.solutions = np.array([self.solutions[i] for x, i in profits_with_index])
        self.profits = np.array([self.profits[i] for x, i in profits_with_index])
