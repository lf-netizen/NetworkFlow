import numpy as np
import copy
from typing import Dict, List
import random
from network import Network
from custom_types import ID


class OptimizationModel:

    routing_tables = Dict[int, Dict[int, int]]
    path = List[int]
    AdjMatrix = np.ndarray

    def __init__(self, network: Network, adjmatrix: AdjMatrix):
        self.network = network
        self.adjmatrix = adjmatrix

    def find_random_path(self, start_vertex: ID, end_vertex: ID) -> path:
        """
        Finds a random path between start_vertex and end_vertex in a Graph using dfs algorithm'
        """
        def dfs(adjmatrix, start_vertex: ID, end_vertex: ID, path: List[ID], visited: List[ID]):
            path = path + [start_vertex]
            if start_vertex == end_vertex:
                return path
            visited.append(start_vertex)
            adj_vertices = [Vertex_ID for Vertex_ID, _ in enumerate(adjmatrix) if adjmatrix[start_vertex][Vertex_ID] == 1]
            random.shuffle(adj_vertices)
            for vertex in adj_vertices:
                if vertex not in visited:
                    new_path = dfs(adjmatrix, vertex, end_vertex, path, visited)
                    if new_path:
                        return new_path
            return None
        path = dfs(self.adjmatrix, start_vertex, end_vertex, [], [])
        if path:
            return path
        else:
            raise KeyError('Network is not connected')

    def create_random_solution(self) -> routing_tables:
        """
        Creates a random matrix representing a legal and acyclic connection between servers and PC's

        inputs:
        m - number of receivers
        n - number of routers
        G - adjacency matrix showing connections between routers and PC's

        outputs:
        random routing_tables
        """
        routing_tables = {}
        for router_id in self.network.routers.keys():
            routing_tables[router_id] = {}
        for router_id in self.network.routers.keys():
            for endpoint_id in self.network.endpoints.keys():
                path = self.find_random_path(router_id, endpoint_id)
                for path_stage, router_in_path in enumerate(path[:-1]):
                    routing_tables[router_in_path][endpoint_id] = path[path_stage+1]
        return routing_tables

    def is_acyclic(self, current_solution: routing_tables) -> bool:
        """
        Checks if current solution is acyclic

        inputs:
        current_solution - current best solution for the algorithm
        G - adjacency matrix showing connections between routers and PC's

        outputs:
        bool value - true if no cycles were found
        """
        #checking all possible connections between PC's
        for endpoint_id in self.network.endpoints.keys():
            for router_id in self.network.routers.keys():
                visited = [router_id]
                #check if current router was added to visited array until we reach the target index
                while router_id != endpoint_id:
                    next_router_id = current_solution[router_id][endpoint_id]
                    if next_router_id in visited:
                        return False
                    else:
                        router_id = next_router_id
                        visited.append(next_router_id)
        return True

    def change_solution(self, current_solution: routing_tables) -> routing_tables:
        """
        Changes random value in the current_solution matrix and checks if this solution is possible

        inputs:
        current_solution - current best solution for the algorithm
        G - adjacency matrix showing connections between routers and PC's

        outputs:
        current_solution - new_solution
        """
        current_solution_copy = copy.deepcopy(current_solution)
        while True:
            router_connection_to_change = random.choice(list(current_solution.keys()))
            endpoint_directory_to_change = random.choice(list(current_solution[router_connection_to_change].keys()))
            new_directory = random.choice(list(self.network.routers.keys()))
            previous_directory = current_solution_copy[router_connection_to_change][endpoint_directory_to_change]
            #checking if there is connection between router y and new directory
            if self.adjmatrix[router_connection_to_change][new_directory] == 1:
                #checking if new solution is acyclic
                current_solution_copy[router_connection_to_change][endpoint_directory_to_change] = new_directory
                if self.is_acyclic(current_solution_copy):
                    current_solution[router_connection_to_change][endpoint_directory_to_change] = new_directory
                    return current_solution
                else:
                    current_solution_copy[router_connection_to_change][endpoint_directory_to_change] = previous_directory

    def run_model(self, t0: float = 0.95, t1: float = 0.001, alpha: float = 0.5, epoch_size: int = 10):
        """
        Minimizes loss function using simulated annealing

        inputs:
        t - array of length n containing cost related to using a particular router in the path
        T0 - starting temperature in the simulated annealing algorithm
        T1 - temperature at which the algorithm stops
        alpha - parameter used to change T after every iteration

        outputs:
        x - solution: optimal routing table
        cost - array representing loss_function values at every iteration
        """
        #creating a random solution
        x = self.create_random_solution()
        cost = []
        t = t0
        previous_loss = self.network.simulate(20)
        while t1 < t:
            for _ in range(epoch_size):
                x1 = self.change_solution(x)
                self.network.load_routing_tables(x1)
                new_loss = self.network.simulate(20)
                if new_loss < previous_loss:
                    x = x1
                    previous_loss = new_loss
                else:
                    probability = np.exp((new_loss - previous_loss)/t)
                    if probability > np.random.random():
                        x = x1
                        previous_loss = new_loss
                Model.network.reset_state(with_schedule=False)
                cost.append(x)
            t = t * alpha
        return x, cost


if __name__ == '__main__':
    adjmatrix = np.array([[0, 1, 1, 0, 0, 0, 1],
                  [1, 0, 1, 1, 0, 0, 0],
                  [1, 1, 0, 0, 1, 1, 0],
                  [0, 1, 0, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0, 0, 0],
                  [1, 0, 0, 0, 0, 0, 0]], dtype=object)
    arch = {
        'routers': [
            {'id': 0, 'transmission_capacity':  5},
            {'id': 1, 'transmission_capacity': 10},
            {'id': 2, 'transmission_capacity': 10}
        ],
        'endpoints': [
            {'id': 3, 'gate_id': 1},
            {'id': 4, 'gate_id': 2},
            {'id': 5, 'gate_id': 2},
            {'id': 6, 'gate_id': 0}
        ]
    }

    schedule = {
        3: [
            {'destination_id': 4,      'request_time': 1, 'priority': 2},
            {'destination_id': [4, 5], 'request_time': 1, 'priority': 2},
            {'destination_id': 6,      'request_time': 3, 'priority': 1}
        ],
        4: [
            {'destination_id': 3,      'request_time': 1, 'priority': 1}
        ]
    }

    # example pipeline
    network = Network(arch)
    network.load_schedule(schedule)
    Model = OptimizationModel(network=network, adjmatrix=adjmatrix)
    print(Model.create_random_solution())
    solution, cost_array = Model.run_model()
    print(solution, cost_array)