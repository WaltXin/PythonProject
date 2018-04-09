class Agent(object):
    def __init__(self):
        self.solution = None
        self.profit = None
        self.interaction = None
        self.fitness = None
        self.nutrient = 0

    @classmethod
    def with_solution(cls, solution):
        agent = cls()
        agent.solution = solution
        return agent
