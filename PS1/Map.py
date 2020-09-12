from math import sqrt
from copy import deepcopy
from operator import itemgetter
from enum import Enum
import matplotlib.pyplot as plt


class AgentType(Enum):
    A = 'A'
    B = 'B'
    EMPTY = '_'
    def __str__(self):
        return self.value


class Agent:
    @staticmethod
    def swap(agent_x, agent_y):
        mid_x = (agent_x.position[0]+agent_y.position[0])/2
        plt.annotate("swapping", (*agent_x.position, 0), xytext=(mid_x,
                                                                 -0.004), arrowprops={'arrowstyle': '->'})
        plt.annotate("swapping", (*agent_y.position, 0), xytext=(mid_x,
                                                                 -0.004), arrowprops={'arrowstyle': '->'})
        temp = deepcopy(agent_x.position)
        agent_x.position = agent_y.position
        agent_y.position = temp

    def __init__(self, coords: list, agent_type: AgentType):
        self.position = coords
        self.agent_type = agent_type


class Map:
    @staticmethod
    def distance(agent1, agent2):
        assert len(agent1.position) == len(agent2.position)
        return sqrt(sum(((agent1.position[i] - agent2.position[i])**2 for i in range(len(agent1.position)))))

    @staticmethod
    def from_string(agents_string):
        return Map([Agent([idx], AgentType(agent_type))for idx, agent_type in enumerate(agents_string)])

    def __init__(self, agents: list):
        self.agents = agents

    def __str__(self):
        map_str = "Map with agents: \n"
        for a in self.agents:
            map_str += "Agent at position " + str(a.position) + "\n"
        return map_str

    def plot(self):
        # print(self.get_coords())
        for a in self.agents:
            color = 'r' if a.agent_type == AgentType.A else 'g' if a.agent_type == AgentType.B else 'b'
            plt.scatter(a.position, 0, c=color)
            plt.annotate(str(a.agent_type), (*a.position, 0), xytext=(*a.position,
                                                                      0.001), rotation=60, arrowprops={'arrowstyle': '->'})
        plt.show()

    def get_coords(self):
        return [a.position for a in self.agents]

    def get_type(self, agent_type):
        return list(filter(lambda a: a.agent_type == agent_type, self.agents))

    def dist_to_type(self, agent, agent_type):
        others = self.get_type(agent_type)
        others = filter(lambda other_agent: other_agent is not agent, others)
        return min((Map.distance(agent, other_agent) for other_agent in others))

    def avoid_other_type(self, agent, other_type):
        # Swap it with empty locales further from the other types
        swappable = self.get_type(AgentType.EMPTY)
        furthest_swappable = max(
            swappable, key=lambda swap_agent: self.dist_to_type(swap_agent, other_type))
        if self.dist_to_type(agent, other_type) < self.dist_to_type(furthest_swappable, other_type):
            # print('hey', agent.agent_type)
            print(
                f"swapping agents at {agent.position}, {furthest_swappable.position}""")
            Agent.swap(agent, furthest_swappable)
            return True
        return False

    def weighted_preference(self, agent, pref_type, other_type, pref_weight, other_weight):
        # Score a position based on its closeness to its preferred type and distance from other type (higher is better)
        return -1 * pref_weight*self.dist_to_type(agent, pref_type) + other_weight*self.dist_to_type(agent, other_type)

    def move(self, agent: Agent, other_type: str, in_weight: float = 1, out_weight: float = 1):
        swappable = self.get_type(AgentType.EMPTY)
        swappable_weights = {s: self.weighted_preference(
            s, agent.agent_type, other_type, in_weight, out_weight) for s in swappable}
        best_swappable = max(swappable_weights.items(),
                             key=itemgetter(1))[0]

        if self.weighted_preference(agent, agent.agent_type, other_type, in_weight, out_weight) < swappable_weights[best_swappable]:
            # print(
            #     f"swapping agents at {agent.position}, {best_swappable.position}""")
            Agent.swap(agent, best_swappable)
            return True
        return False

    def move_all(self, in_weight=1, out_weight=1):
        agents = sorted(self.agents, key=lambda a: a.position)
        moved_any = False
        for a in filter(lambda a: a.agent_type != AgentType.EMPTY, agents):
            other_type = AgentType.A if a.agent_type == AgentType.B else AgentType.B
            a_moved = self.move(a, other_type, in_weight, out_weight)
            if a_moved:
                moved_any = True
                self.plot()
        return moved_any

    def schelling(self, in_weight=1, out_weight=1):
        runtime = 0
        moved_any = True
        self.plot()
        while moved_any:
            some_moved = self.move_all(in_weight, out_weight)
            if not some_moved:
                moved_any = False
                self.plot()
            runtime += 1
            if runtime > 100:
                print("There may not be a stable arrangement")
                break


if __name__ == "__main__":
    m = Map.from_string('ABABAB_')
    # print(m)
    # m.plot()
    m.schelling()
    # m.plot()
