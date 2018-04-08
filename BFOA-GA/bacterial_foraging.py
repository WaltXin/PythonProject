import numpy as np
from random import random

worst_profit = -1


class BacterialForaging(object):
    def __init__(self, evaluate, create_initial, is_solution_valid, num_agents, num_dimensions, num_iterations,
                 num_steps=2, swim_len=12, step_size=0.2, eliminate_probability=1.15):

        self.evaluate = evaluate
        self.create_initial = create_initial
        self.is_solution_valid = is_solution_valid
        self.num_agents = num_agents
        self.num_dimensions = num_dimensions
        self.num_iterations = num_iterations
        self.num_steps = num_steps
        self.swim_len = swim_len
        self.step_size = step_size
        self.eliminate_probability = eliminate_probability

        self.agents = [create_initial() for _ in range(num_agents)]
        self.profits = self.evaluate_agents(self.agents)

        self.iteration_best = []
        self.iteration_best_profit = worst_profit
        self.global_best = []
        self.global_best_profit = worst_profit

        self.compute_best()

        self.step_list = [step_size - step_size * 0.9 * i / num_iterations for i in range(num_iterations)]
        self.eliminate_list = [eliminate_probability - eliminate_probability * 0.5 * i / num_iterations
                               for i in range(num_iterations)]

        self.previous_profit = self.profits[::1]

    def evaluate_agents(self, agents):
        return np.array([self.evaluate(x) for x in agents])

    def compute_best(self):
        best_agent = self.profits.argmax()
        self.iteration_best = self.agents[best_agent]
        self.iteration_best_profit = self.profits[best_agent]

        if self.iteration_best_profit > self.global_best_profit:
            self.global_best = self.iteration_best
            self.global_best_profit = self.iteration_best_profit

    def iterate(self, iteration):
        chem_profits = [self.profits[::1]]

        for j in range(self.num_steps):
            for i in range(self.num_agents):
                dell = np.random.uniform(-1, 1, self.num_dimensions)
                delta = self.step_list[iteration] * np.linalg.norm(dell) * dell
                self.agents[i] = to_0_1(self.agents[i] + delta)

                for m in range(self.swim_len):
                    if self.evaluate(self.agents[i]) > self.previous_profit[i]:
                        self.previous_profit[i] = self.profits[i]
                        self.agents[i] = to_0_1(self.agents[i] + delta)
                    else:
                        dell = np.random.uniform(-1, 1, self.num_dimensions)
                        delta = self.step_list[iteration] * np.linalg.norm(dell) * dell
                        self.agents[i] = to_0_1(self.agents[i] + delta)

            self.profits = self.evaluate_agents(self.agents)
            chem_profits += [self.profits]

        chem_profits = np.array(chem_profits)

        health = [(sum(chem_profits[:, i]), i) for i in range(self.num_agents)]
        health.sort(reverse=True)
        alive_agents = []
        for i in health:
            alive_agents += [list(self.agents[i[1]])]

        if self.num_agents & 1:
            alive_agents = 2 * alive_agents[:self.num_agents // 2]
            self.agents = np.array(alive_agents)
        else:
            alive_agents = 2 * alive_agents[:self.num_agents // 2] + [alive_agents[self.num_agents // 2]]
            self.agents = np.array(alive_agents)

        if iteration < self.num_iterations - 2:
            for i in range(self.num_agents):
                r = random()
                if r >= self.eliminate_list[iteration]:
                    self.agents[i] = self.create_initial()

        self.profits = self.evaluate_agents(self.agents)

        self.compute_best()


def to_0_1(v):
    return ((v.astype(int) % 2) + 2) % 2
