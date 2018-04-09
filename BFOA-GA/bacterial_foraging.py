import numpy as np

import mkp_agent


class BacterialForaging(object):
    def __init__(self, evaluate, create_initial, is_solution_valid, num_agents, num_dimensions, num_iterations,
                 elim_disp_steps=1, repro_steps=2, chem_steps=20, swim_len=4, step_size=0.05,
                 d_attr=0.1, w_attr=0.2, h_rep=0.1, w_rep=10, p_eliminate=0.25):

        self.compute_profit = evaluate
        self.create_initial = create_initial
        self.is_solution_valid = is_solution_valid
        self.num_agents = num_agents
        self.num_dimensions = num_dimensions
        self.num_iterations = num_iterations
        self.elim_disp_steps = elim_disp_steps
        self.repro_steps = repro_steps
        self.chem_steps = chem_steps
        self.swim_len = swim_len
        self.step_size = step_size
        self.d_attr = d_attr
        self.w_attr = w_attr
        self.h_rep = h_rep
        self.w_rep = w_rep
        self.p_eliminate = p_eliminate

        self.agents = None

    def create_agent(self, agents, solution):
        agent = mkp_agent.Agent()
        agent.solution = solution
        agent.profit = self.compute_profit(solution)
        agent.interaction = self.compute_interaction(agents, solution)
        agent.fitness = agent.profit + agent.interaction
        return agent

    def compute_interaction(self, agents, solution):
        attract = self.compute_interaction_with_parameters(agents, solution, self.d_attr, -self.w_attr)
        repel = self.compute_interaction_with_parameters(agents, solution, -self.h_rep, -self.w_rep)
        return attract + repel

    @staticmethod
    def compute_interaction_with_parameters(agents, solution, d, w):
        return d * np.sum([np.exp(w * norm_sq(solution - other.solution)) for other in agents])

    def iterate(self, iteration, solutions, profits):
        self.agents = [mkp_agent.Agent.with_solution(solution) for solution in solutions]
        self.agents = [self.create_agent(self.agents, agent.solution) for agent in self.agents]

        for elim_disp in range(self.elim_disp_steps):
            for repro in range(self.repro_steps):
                for chem in range(self.chem_steps):
                    self.agents = [self.chemotaxis(agent) for agent in self.agents]

                # reproduction
                self.agents.sort(key=lambda agent: agent.nutrient, reverse=True)
                self.agents = self.agents[:self.num_agents >> 1] * 2

            # elimination-dispersal
            for agent_index, agent in enumerate(self.agents):
                if np.random.rand() <= self.p_eliminate:
                    self.agents[agent_index] = self.create_agent(self.agents, self.create_initial())

        solutions = np.array([agent.solution for agent in self.agents])
        profits = np.array([agent.profit for agent in self.agents])
        return solutions, profits

    def chemotaxis(self, agent):
        nutrient = agent.fitness

        for m in range(self.swim_len):
            new_solution = self.tumble(agent.solution)
            new_agent = self.create_agent(self.agents, new_solution)
            if new_agent.fitness < agent.fitness:
                break

            agent = new_agent
            nutrient += agent.fitness

        agent.nutrient = nutrient
        return agent

    def tumble(self, solution):
        new_solution = np.zeros(solution.shape, dtype=solution.dtype)
        for i in range(self.num_dimensions):
            if np.random.rand() <= self.step_size:
                new_solution[i] = 1 - solution[i]
            else:
                new_solution[i] = solution[i]
        return new_solution


def norm_sq(x):
    return np.dot(x, x)


def to_0_1(v):
    return ((v.astype(int) % 2) + 2) % 2
