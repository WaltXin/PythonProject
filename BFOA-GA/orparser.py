import numpy as np
import scanner


class Problem(object):
    def __init__(self):
        self.num_items = 0
        self.num_limits = 0
        self.optimum = 0
        self.profits = []
        self.weights = []
        self.limits = []


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
