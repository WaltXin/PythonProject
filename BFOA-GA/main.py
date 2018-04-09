import numpy as np
import sys

import bacterial_foraging
import genetic
import mkp_result
import mkp_work_unit
import orparser

num_iterations = 100
num_ga_agents = 500
num_bfoa_agents = 30
problem_file = 'orlib/mknap_sikessle.txt'

algo = sys.argv[1] if len(sys.argv) > 1 else None
bfoa_enabled = algo == 'bfoa' or algo == 'ga-bfoa' or algo is None
ga_enabled = algo == 'ga' or algo == 'ga-bfoa' or algo is None


def main():
    problems = orparser.parse(problem_file)
    problem = problems[0]

    work_unit = create_work_unit(problem)
    result = mkp_result.Result()

    bfoa = bacterial_foraging.BacterialForaging(
        problem.compute_profit, problem.create_initial, problem.is_solution_valid,
        num_agents=num_bfoa_agents, num_dimensions=problem.num_items, num_iterations=num_iterations)
    ga = genetic.Genetic(
        problem.compute_profit, problem.create_initial, problem.is_solution_valid,
        num_agents=num_ga_agents, num_dimensions=problem.num_items, num_iterations=num_iterations)

    for iteration in range(num_iterations):
        if ga_enabled:
            output = ga.iterate(iteration, *work_unit.get_best(num_ga_agents))
            work_unit.replace_worst(*output)

        if bfoa_enabled:
            output = bfoa.iterate(iteration, *work_unit.get_best(num_bfoa_agents))
            work_unit.replace_worst(*output)

        result.compute_best(work_unit.solutions, work_unit.profits)
        print(result.best_profit)

    print('result : {}'.format(result.best_profit))
    print('optimum: {}'.format(problem.optimum))


def create_work_unit(problem):
    num_agents = max(num_ga_agents, num_bfoa_agents)
    solutions = np.array([problem.create_initial() for _ in range(num_agents)])
    profits = np.array([problem.compute_profit(solution) for solution in solutions])
    return mkp_work_unit.WorkUnit(solutions, profits)


main()
