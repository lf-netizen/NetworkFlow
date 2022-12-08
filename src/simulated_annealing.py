import numpy as np
import copy
from typing import Dict, List
import random
from devices import Endpoint
from custom_types import ID
routings_table = Dict[int,Dict[int,int]]
path = List[int]
AdjMatrix = np.ndarray


def find_random_path(G:AdjMatrix, start_vertex:ID, end_vertex:ID) -> path:
    '''
    Finds a random path between start_vertex and end_vertex in a Graph using dfs algorithm'
    '''
    def dfs(G:np.ndarray, start_vertex:ID, end_vertex:ID, path:List[ID], visited:List[ID]):
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return path
        visited.append(start_vertex)
        adj_vertices = [Vertex_ID for Vertex_ID,_ in enumerate(G) if G[start_vertex][Vertex_ID] == 1]
        random.shuffle(adj_vertices)
        for vertex in adj_vertices:
            if vertex not in visited:
                new_path = dfs(G, vertex, end_vertex, path, visited)
                if new_path:
                    return new_path
        return None
    path = dfs(G, start_vertex, end_vertex, [], [])
    if path:
        return path
    else:
        raise ValueError('Network is not connected')


def create_random_solution(endpoints_ids:List[ID],routers_ids:List[ID], G:AdjMatrix) -> routings_table:
    '''
    Creates a random matrix representing a legal and acyclic connection between servers and PC's
    
    inputs: 
    m - number of reveivers
    n - number of routers
    G - adjacency matrix showing connections between routers and PC's

    outputs:
    random routing_tables
    '''
    routing_tables = {}
    for router_id in routers_ids:
        routing_tables[router_id] = {}
    for router_id in routers_ids:
        for endpoint_id in endpoints_ids:
            path = find_random_path(G, router_id, endpoint_id)
            print(f'start: {router_id}, end: {endpoint_id}, path: {path}')
            for path_stage,router_in_path in enumerate(path[:-1]):
                routing_tables[router_in_path][endpoint_id] = path[path_stage+1]
    return routing_tables


def is_acyclic(endpoints_ids:List[ID],routers_ids:List[ID],current_solution:routings_table,G:AdjMatrix) -> bool:
    '''
    Checks if current solution is acyclic
    
    inputs: 
    current_solution - current best solution for the algorithm
    G - adjacency matrix showing connections between routers and PC's

    outputs:
    bool value - true if no cycles were found
    '''

    #checking all possible connections between PC's 
    for endpoint_id in endpoints_ids:
        for router_id in routers_ids:
            visited = [router_id]
            #check if current router was added to visited array until we reach the target index
            while(router_id != endpoint_id):
                next_router_id = current_solution[router_id][endpoint_id]
                if(next_router_id in visited):
                    return False
                else:
                    router_id = next_router_id
                    visited.append(next_router_id)
    return True


def change_solution(endpoints_ids:List[ID], routers_ids:List[ID],current_solution:routings_table, G:AdjMatrix) -> routings_table:
    '''
    Changes random value in the current_solution matrix and checks if this solution is possible

    inputs: 
    current_solution - current best solution for the algorithm
    G - adjacency matrix showing connections between routers and PC's

    outputs:
    current_solution - new_solution
    '''
    current_solution_copy = copy.deepcopy(current_solution)
    while(True):
        router_connection_to_change = random.choice(list(current_solution.keys()))
        endpoint_directory_to_change = random.choice(list(current_solution[router_connection_to_change].keys()))
        new_directory = random.choice(routers_ids)
        previous_directory = current_solution_copy[router_connection_to_change][endpoint_directory_to_change]
        #checking if there is connection between router y and new directory
        if G[router_connection_to_change][new_directory] == 1:
            #checking if new solution is acyclic
            current_solution_copy[router_connection_to_change][endpoint_directory_to_change] = new_directory
            if is_acyclic(endpoints_ids, routers_ids, current_solution_copy, G):
                current_solution[router_connection_to_change][endpoint_directory_to_change] = new_directory
                return current_solution
            else:
                current_solution_copy[router_connection_to_change][endpoint_directory_to_change] = previous_directory


def simulated_annealing(loss_fun:callable, m:int, n:int, G:AdjMatrix, T0:float = 0.95, T1:float = 0.001, alpha:float = 0.5, epoch_size:int = 10):
    '''
    Minimizes loss function using simulated annealing

    inputs:
    m - number of reveivers
    n - number of routers
    G - adjacency matrix showing connections between routers
    t - array of length n containing cost related to using a particular router in the path
    T0 - starting temperature in the simulated annealing algorithm
    T1 - temperature at which the algorithm stops
    alpha - paramter used to change T after every iteration

    outputs:
    x - solution: np.ndarray of shape(m,n+m) where values represent indices of routers to which packages should be sent, 
    rows represent the target reveiver and column represents index of current server/PC where the package is
    cost - array representing loss_function values at every iteration
    '''
    #creating a random solution
    x = create_random_solution(m,n,G)
    cost = []
    T = T0
    while(T1 < T):
        for _ in range(epoch_size):
            x1 = change_solution(x,G)
            if loss_fun(x1) < loss_fun(x):
                x = x1
            else:
                probability = np.exp((loss_fun(x1) - loss_fun(x))/T)
                if probability > np.random.random():
                    x = x1
            cost.append(x)
        T = T * alpha
    return x, cost

if __name__ == '__main__':
    G = np.array([[0, 1, 1, 0, 0, 0, 1],
                  [1, 0, 1, 1, 0, 0, 0],
                  [1, 1, 0, 0, 1, 1, 0],
                  [0, 1, 0, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0, 0, 0],
                  [1, 0, 0, 0, 0, 0, 0]], dtype=object)
    e1 = Endpoint(id=3, gate_id=1)
    e2 = Endpoint(id=4, gate_id=3)
    e3 = Endpoint(id=5, gate_id=3)
    e4 = Endpoint(id=6, gate_id=0)
    random_solution = create_random_solution(endpoints_ids=[3, 4, 5, 6],routers_ids=[0,1,2], G=G)
    print(random_solution)
    print(is_acyclic([3,4,5,6], [0,1,2], random_solution, G))
    print(change_solution([3,4,5,6], [0,1,2], random_solution, G))

