import numpy as np


class Genetic(object):
    def __init__(self, compute_profit, create_initial, is_solution_valid, num_agents, num_dimensions, num_iterations,
                 mutate_probability=0.3, offsprings_proportion=0.5):

        self.compute_profit = compute_profit
        self.create_initial = create_initial
        self.is_solution_valid = is_solution_valid
        self.num_agents = num_agents
        self.num_dimensions = num_dimensions
        self.iteration = num_iterations
        self.mutate_probability = mutate_probability
        self.num_agents = num_agents
        self.offsprings_proportion = offsprings_proportion

        self.num_offspring_pairs = int(offsprings_proportion * num_agents) >> 1

        self.solutions = None
        self.profits = None

        self.agent_indices = np.arange(self.num_agents)

    def compute_profits(self, solutions):
        return np.array([self.compute_profit(x) for x in solutions])

    def iterate(self, iteration, solutions, profits):
        self.solutions = solutions
        self.profits = profits

        probabilities = self.compute_probabilities()
        offsprings = np.zeros((self.num_offspring_pairs * 2, self.num_dimensions), dtype=int)

        i = 0
        while i < self.num_offspring_pairs:
            parents = self.get_parents(probabilities)
            a, b = self.get_offspring_pair(parents)
            if a is not None:
                offsprings[i * 2] = a
                offsprings[i * 2 + 1] = b
                i += 1

        self.replace_worst(offsprings)

        return self.solutions, self.profits

    def compute_probabilities(self):
        total_profits = float(self.profits.sum())
        return self.profits / total_profits

    def get_parents(self, probabilities):
        i, j = np.random.choice(self.agent_indices, size=2, replace=False, p=probabilities)
        return self.solutions[i], self.solutions[j]

    def get_offspring_pair(self, parents):
        a = np.zeros(self.num_dimensions, dtype=int)
        b = np.zeros(self.num_dimensions, dtype=int)

        for i in range(self.num_dimensions):
            parent_index = 0 if np.random.rand() <= 0.5 else 1
            a[i] = parents[parent_index][i]
            b[i] = parents[1 - parent_index][i]

        self.mutate(a)
        self.mutate(b)

        if self.is_solution_valid(a) and self.is_solution_valid(b):
            return a, b
        else:
            return None, None

    def mutate(self, solution):
        if np.random.rand() > self.mutate_probability:
            return

        i = np.random.randint(self.num_dimensions)
        solution[i] = 1 - solution[i]

    def replace_worst(self, offsprings):
        solutions = np.concatenate([self.solutions, offsprings])

        offspring_profits = self.compute_profits(offsprings)
        profits = np.concatenate([self.profits, offspring_profits])

        profits_with_index = [(x, i) for i, x in enumerate(profits)]
        profits_with_index.sort(reverse=True)
        profits_with_index = profits_with_index[:self.num_agents]

        self.solutions = np.array([solutions[i] for x, i in profits_with_index])
        self.profits = np.array([profits[i] for x, i in profits_with_index])
