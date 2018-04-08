import numpy as np

import bacterial_foraging
import genetic
import orparser

problems = orparser.parse('orlib/mknap_sikessle.txt')
p = next(x for x in problems if x.optimum > 0)

low = 0
high = 2
num_dimensions = p.num_items
num_iterations = 200
worst_profit = -1


def evaluate(solution):
    for limit in range(p.num_limits):
        weights = p.weights[limit]
        total_weight = np.sum(weights * solution)

        if total_weight > p.limits[limit]:
            return worst_profit

    return np.sum(p.profits * solution)


def create_initial():
    solution = np.random.randint(low, high, num_dimensions)
    make_solution_valid(solution)
    return solution


def is_solution_valid(solution):
    return evaluate(solution) != worst_profit


def make_solution_valid(solution):
    while not is_solution_valid(solution):
        solution[np.random.randint(0, len(solution) - 1)] = 0


bfoa = bacterial_foraging.BacterialForaging(evaluate, create_initial, is_solution_valid,
                                            num_agents=40, num_dimensions=num_dimensions, num_iterations=num_iterations)
ga = genetic.Genetic(evaluate, create_initial, is_solution_valid,
                     num_agents=1000, num_dimensions=num_dimensions, num_iterations=num_iterations)
print("BFOA    GA")
for iteration in range(num_iterations):
    bfoa.iterate(iteration)
    ga.iterate(iteration)
    print(bfoa.global_best_profit, ga.global_best_profit)

print(max(bfoa.global_best_profit, ga.global_best_profit))
print(p.optimum)
