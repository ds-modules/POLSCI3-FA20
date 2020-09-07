# class Agent:
#     def __init__(self, group_id, x, y, ingroup_frac):
#         self.x, self.y = x, y
#         self.group_id = group_id

#     def is_satisfied(self, model):
#         pass


from random import randint, choice, shuffle, uniform
from math import floor, sqrt, ceil
import matplotlib.pyplot as plt
from copy import deepcopy
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
        self.location = uniform(0, 1), uniform(0, 1)

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


def empty_idxs(lst):
    return [i for i in range(len(lst)) if lst[i] == '_']


def total_neighbors(idx, lst):
    n_count = 0
    if idx > 0 and lst[idx-1] != '_':
        n_count += 1
    if idx < len(lst)-1 and lst[idx+1] != '_':
        n_count += 1
    return n_count


def group_count(idx: int, group_type: str, lst) -> int:
    g_count = 0
    if idx > 0 and lst[idx-1] == group_type:
        g_count += 1
    if idx < len(lst)-1 and lst[idx+1] == group_type:
        g_count += 1
    return g_count


def dist_to_group(idx: int, group_type: str, lst):
    """
    A version of group_count that allows for sorting with solo agents
    Sometimes entities don't have immediately adjacent neighbors. 
    In that case, the value represents the distance to any neighbor, e.g
    -1 means that an entity one to the left or right has a neighbor of that type.

    Args:
        idx (int):index in the list
        group_type (str):group type we care about matching
        lst ([type]): [description]
    """
    my_count = group_count(idx, group_count, lst)
    if my_count > 0:
        return my_count
    adjacent_counts = []
    l_neighbor_count = dist_to_group(idx-1, group_type, lst) if idx > 0 else None
    r_neighbor_count = dist_to_group(idx+1, group_type, lst) if idx < len(lst)-1  else None
    for neighbor_count in (l_neighbor_count, r_neighbor_count):
        if neighbor_count != 0:
            if neighbor_count < 0 and neighbor_count is not None: #The neighbor doesn't have any next directly to it either 
                adjacent_counts.append(neighbor_count - 1)
            else: #The neighbor does have one next to it!
                adjacent_counts.append(neighbor_count) 
    return max(adjacent_counts)


def swap(idx: int, idy: int, lst: list):
    """Swap in place the values at idx and idy

    Args:
        idx (int): first index
        idy (int): second index
        lst (list): the list
    """
    temp = lst[idx]
    lst[idx] = lst[idy]
    lst[idy] = temp


# def move(idx, members_lst):
#     if members_lst[idx] == 'A':
#         current_b = other_neighbor_count(idx, members_lst)
#         # print(current_b)
#         for e_idx in empty_idxs(members_lst):
#             # print(e_idx)
#             empty_b_count = other_neighbor_count(e_idx, members_lst)
#             # print(empty_b_count)
#             if empty_b_count < current_b:
#                 swap(e_idx, idx, members_lst)
#                 current_b = empty_b_count
#     if members_lst[idx] == 'B':
#         current_n = total_neighbors(idx, members_lst)
#         for e_idx in empty_idxs(members_lst):
#             empty_n_count = total_neighbors(e_idx, members_lst)
#             if empty_n_count > current_n:
#                 swap(e_idx, idx, members_lst)
#                 current_n = empty_n_count
# def stable_alignment(members_lst: [str]) -> bool:
#     for member in members_lst:


def avoid_others(idx, members_lst):
    other_type = 'B' if members_lst[idx] == 'A' else 'A'
    current_others = group_count(idx, other_type, members_lst)
    # print(current_b)
    # for e_idx in empty_idxs(members_lst):
    #     # print(e_idx)
    #     empty_others_count = other_neighbor_count(
    #         e_idx, other_type, members_lst)
    #     # print(empty_b_count)
    #     if empty_others_count < current_others:
    #         swap(e_idx, idx, members_lst)
    #         current_others = empty_others_count
    empty_others_counts = [(e_idx, dist_to_group(
        e_idx, other_type, members_lst)) for e_idx in empty_idxs(members_lst)]
    empty_others_counts = sorted(
        empty_others_counts, key=lambda tup: tup[1])
    print(members_lst[idx], empty_others_counts)
    if empty_others_counts[0][1] < current_others:
        swap(idx, empty_others_counts[0][0], members_lst)


def increase_ingroup(idx, members_lst):
    current_ingroup_count = group_count(idx, members_lst[idx], members_lst)
    empty_ingroup_counts = [(e_idx, dist_to_group(
        e_idx, members_lst[idx], members_lst)) for e_idx, val in enumerate(empty_idxs(members_lst))]
    empty_ingroup_counts = sorted(
        empty_ingroup_counts, key=lambda tup: tup[1], reverse=True)
    if empty_ingroup_counts[0][1] < current_ingroup_count:
        swap(idx, empty_ingroup_counts[0][0], members_lst)


def move_all(members_lst):
    print(members_lst)
    past_lst = deepcopy(members_lst)
    for member_idx in range(len(members_lst)):
        if past_lst[member_idx] != '_':
            avoid_others(member_idx, members_lst)
            print(members_lst)
            past_lst = deepcopy(members_lst)


def schelling(members_str):
    runtime = 0
    members = list(members_str)
    old_lst = []
    while old_lst != members:
        old_lst = deepcopy(members)
        move_all(members)
        runtime += 1
        if runtime > 100:
            print("There may not be a stable arrangement")
            break


if __name__ == "__main__":
    schelling(['A', 'B', 'A', 'B', 'A', 'B', '_', '_', '_'])
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
