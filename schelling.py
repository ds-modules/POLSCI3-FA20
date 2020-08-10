# class Agent:
#     def __init__(self, group_id, x, y, ingroup_frac):
#         self.x, self.y = x, y
#         self.group_id = group_id

#     def is_satisfied(self, model):
#         pass


from random import randint, choice, shuffle, uniform
from math import floor, sqrt, ceil
import matplotlib.pyplot as plt

from itertools import product
# class Model:

#     def __init__(self, n: int, a_prop: float, b_prop: float, ingroup_frac: float):
#         """Init

#         Args:
#             n (int): grid size
#             a_prop (float): what percentage of pop is an A
#             b_prop (float): what percentage of pop is a B
#             ingroup_frac (float): [description]
#         """
#         assert a_prop + b_prop <= 1
#         self.n, self.a_prop, self.b_prop, self.ingroup_frac = n, a_prop, b_prop, ingroup_frac
#         self.grid = [[None for _ in range(n)] for _ in range(n)]
#         a_count, b_count = 0, 0
#         while a_count < floor(self.n**2*self.a_prop):
#             shuffle(self.grid)
#             for sublist in self.grid:
#                 shuffle(sublist)
#             if self.grid[0][0] is None:
#                 self.grid[0][0] = 'A'
#                 a_count += 1
#         while b_count < floor(self.n**2*self.b_prop):
#             shuffle(self.grid)
#             for sublist in self.grid:
#                 shuffle(sublist)
#             if self.grid[0][0] is None:
#                 self.grid[0][0] = 'B'
#                 b_count += 1
#         print(self.all_satisfied())
#         # a_list, b_list = [], []
#         # for i in range(self.n):
#         #     for j in range(self.n):
#         #         new_id = choice(('A', 'B'))
#         #         self.grid[i][j] = new_id
#         #         if new_id == 'A':
#         #             a_count += 1
#         #             a_list.append((j, i))
#         #         else:
#         #             b_count += 1
#         #             b_list.append((j, i))

#         # while a_count > floor(self.n*self.a_prop):
#         #     shuffle(a_list)
#         #     dead_x, dead_y = a_list.pop()
#         #     self.grid[dead_y][dead_x] = None
#         # while b_count > floor(self.n*self.b_prop):
#         #     shuffle(b_list)
#         #     dead_x, dead_y = b_list.pop()
#         #     self.grid[dead_y][dead_x] = None
#         # while a_count < self.n*self.a_prop:
#         #     new_x, new_y = randint(0, self.n-1), randint(0, self.n-1)
#         #     if self.grid[new_y][new_x] is None:
#         #         self.grid[new_y][new_x] = 'A'
#         # while b_count < self.n*self.b_prop:
#         #     new_x, new_y = randint(0, self.n-1), randint(0, self.n-1)
#         #     if self.grid[new_y][new_x] is None:
#         #         self.grid[new_y][new_x] = 'B'

#     def agent_satisfied(self, x, y):
#         agent_id = self.grid[y][x]
#         # print(agent_id, x, y)
#         neighbor_count = 0
#         sat_count = 0
#         for n_y in range(y-1, y+1):
#             for n_x in range(x-1, x+1):
#                 in_bounds = 0 <= n_x <= self.n-1 and 0 <= n_y <= self.n-1
#                 is_agent = x == n_x and y == n_y
#                 # print(in_bounds, is_agent)
#                 if in_bounds and not is_agent and self.grid[n_y][n_x] is not None:
#                     sat_count = sat_count + \
#                         1 if self.grid[n_y][n_x] == agent_id else sat_count
#                     neighbor_count += 1
#         # print(neighbor_count, floor(self.ingroup_frac * neighbor_count))
#         return sat_count >= floor(self.ingroup_frac * neighbor_count)

#     def all_satisfied(self):
#         for i in range(self.n):
#             for j in range(self.n):
#                 if self.grid[i][j] is not None and not self.agent_satisfied(j, i):
#                     return False
#         return True

#     def plot(self):
#         plt.figure()
#         for i in range(self.n):
#             for j in range(self.n):
#                 if self.grid[i][j] == 'A':
#                     plt.plot(j, i, 'bo')
#                 elif self.grid[i][j] == 'B':
#                     plt.plot(j, i, 'go')
#         plt.show()


class Agent:

    def __init__(self, agent_id, agents, n, num_neighbors=10, prop_same=.3):
        self.agent_id = agent_id
        self.num_neighbors = num_neighbors
        self.draw_location(agents, n)
        self.num_same_req = floor(num_neighbors*prop_same)

    def draw_location(self, agents, n):
        # print(agents)
        # used_points = [a.location for a in agents]
        # # print(ceil(sqrt(n)))
        # all_points = list(product(range(ceil(sqrt(n))), repeat=2))
        # # print(len(all_points))
        # valid_points = list(
        #     filter(lambda point: point not in used_points, all_points))
        # shuffle(valid_points)
        # print(valid_points)
        self.location = uniform(0,1), uniform(0,1)

    def get_distance(self, other):
        "Computes the euclidean distance between self and other agent."
        a = (self.location[0] - other.location[0])**2
        b = (self.location[1] - other.location[1])**2
        return sqrt(a + b)

    def happy(self, agents):
        "True if sufficient number of nearest neighbors are of the same agent_id."
        distances = []
        # distances is a list of pairs (d, agent), where d is distance from
        # agent to self
        for agent in agents:
            if self != agent:
                distance = self.get_distance(agent)
                distances.append((distance, agent))
        # == Sort from smallest to largest, according to distance == #
        # print(distances)
        distances.sort(key=lambda tup: tup[0])
        # == Extract the neighboring agents == #
        neighbors = [agent for d, agent in distances[:self.num_neighbors]]
        # == Count how many neighbors have the same agent_id as self == #
        num_same_type = sum(
            self.agent_id == agent.agent_id for agent in neighbors)
        return num_same_type >= self.num_same_req

    def update(self, agents, n):
        "If not happy, then randomly choose new locations until happy."
        while not self.happy(agents):
            self.draw_location(agents, n)


class World:
    def __init__(self, n, zero_prop, one_prop, same_prop=.3):
        num_of_type_0 = floor(n*zero_prop)
        num_of_type_1 = floor(n*one_prop)
        self.n = n
        num_neighbors = 10      # Number of agents regarded as neighbors
        # require_same_type = 5   # Want at least this many neighbors to be same type
        # == Create a list of agents == #
        self.agents = []
        for _ in range(num_of_type_0):
            self.agents.append(
                Agent(0, self.agents, self.n, num_neighbors, same_prop))
        for _ in range(num_of_type_1):
            self.agents.append(
                Agent(1, self.agents, self.n, num_neighbors, same_prop))


    def plot_distribution(self, cycle_num):
        "Plot the distribution of agents after cycle_num rounds of the loop."
        x_values_0, y_values_0 = [], []
        x_values_1, y_values_1 = [], []
        # == Obtain locations of each type == #
        for agent in self.agents:
            x, y = agent.location
            if agent.agent_id == 0:
                x_values_0.append(x)
                y_values_0.append(y)
            else:
                x_values_1.append(x)
                y_values_1.append(y)
        fig, ax = plt.subplots(figsize=(8, 8))
        plot_args = {'markersize': 8, 'alpha': 0.6}
        ax.set_facecolor('azure')
        ax.plot(x_values_0, y_values_0, 'o',
                markerfacecolor='orange', **plot_args)
        ax.plot(x_values_1, y_values_1, 'o',
                markerfacecolor='green', **plot_args)
        ax.set_title(f'Cycle {cycle_num}')
        plt.show()

    def loop(self):
        count = 1
        # ==  Loop until none wishes to move == #
        self.plot_distribution(count)

        while True:
            print('Entering loop ', count)
            count += 1
            no_one_moved = True
            for agent in self.agents:
                old_location = agent.location
                agent.update(self.agents, self.n)
                if agent.location != old_location:
                    no_one_moved = False
            if no_one_moved:
                break
            self.plot_distribution(count)
        print('Converged, terminating.')


if __name__ == "__main__":
    World(500, .5, .5, .7).loop()
    # num_of_type_0 = 250
    # num_of_type_1 = 250
    # num_neighbors = 10      # Number of agents regarded as neighbors
    # require_same_type = 5   # Want at least this many neighbors to be same type

    # # == Create a list of agents == #
    # agents = [Agent(0) for i in range(num_of_type_0)]
    # agents.extend(Agent(1) for i in range(num_of_type_1))

    # count = 1
    # # ==  Loop until none wishes to move == #
    # while True:
    #     print('Entering loop ', count)
    #     plot_distribution(agents, count)
    #     count += 1
    #     no_one_moved = True
    #     for agent in agents:
    #         old_location = agent.location
    #         agent.update(agents)
    #         if agent.location != old_location:
    #             no_one_moved = False
    #     if no_one_moved:
    #         break

    # print('Converged, terminating.')
