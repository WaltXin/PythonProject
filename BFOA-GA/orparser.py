import numpy as np
import scanner

import mkp_result


class Problem(object):
    def __init__(self):
        self.num_items = 0
        self.num_limits = 0
        self.optimum = 0
        self.profits = []
        self.weights = []
        self.limits = []

    def create_initial(self):
        solution = np.random.randint(0, 2, self.num_items)
        self.make_solution_valid(solution)
        return solution

    def compute_profit(self, solution):
        for limit in range(self.num_limits):
            weights = self.weights[limit]
            total_weight = np.sum(weights * solution)

            if total_weight > self.limits[limit]:
                return mkp_result.worst_profit

        return np.sum(self.profits * solution)

    def is_solution_valid(self, solution):
        return self.compute_profit(solution) != mkp_result.worst_profit

    def make_solution_valid(self, solution):
        while not self.is_solution_valid(solution):
            solution[np.random.randint(0, len(solution) - 1)] = 0


def parse(filename):
    with scanner.Scanner(file=filename) as sc:
        num_problems = sc.next_int()
        return [parse_problem(sc) for _ in range(num_problems)]


def parse_problem(sc):
    p = Problem()
    p.num_items = sc.next_int()
    p.num_limits = sc.next_int()
    p.optimum = sc.next_int()
    p.profits = np.array([sc.next_int() for _ in range(p.num_items)])
    p.weights = np.array([[sc.next_int() for _ in range(p.num_items)] for _ in range(p.num_limits)])
    p.limits = np.array([sc.next_int() for _ in range(p.num_limits)])
    return p
