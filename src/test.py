import numpy as np
import random
from typing import List, Dict
ID = int

def generate_random_adjacency_matrix(m: int, n: int, connection_probability: float):
    '''
    m: number of routers
    n: number of computers
    '''
    matrix = [[0 for i in range(m+n)] for j in range(m+n)]
    #connections between routers
    for i in range(m):
        for j in range(m):
            if i != j and np.random.random() > (1-connection_probability):
                matrix[i][j] = 1
                matrix[j][i] = 1
            else:
                matrix[i][j] = 0
                matrix[j][i] = 0

    # connections between routers and computers
    for i in range(n):
        for j in range(m):
            matrix[i+m][j] = 0
            matrix[j][i+m] = 0

    # connections between endpoint and gate
    gate_ids = {}
    for i in range(n):
        endpoint_id = i+m
        gate_id = random.randrange(0, m)
        matrix[endpoint_id][gate_id] = 1
        matrix[gate_id][endpoint_id] = 1
        gate_ids[endpoint_id] = gate_id

    #connections between computers
    for i in range(n):
        for j in range(n):
            matrix[i+m][j+m] = 0

    #generate network architecture
    arch = {
        'routers': [],
        'endpoints': []
    }
    for i in range(m):
        arch['routers'].append({'id': i, 'transmission_capacity':  random.choice([5, 10, 15])})
    for endpoint_id, gate_id in gate_ids.items():
        arch['endpoints'].append({'id': endpoint_id, 'gate_id': gate_id})

    return np.array(matrix, dtype=object), arch

def generate_mean_case(m, n, connection_probability):
    '''
    One network made of 2 network connected by 2 routers
    m: number of routers in one network
    n: number of computers in one network
    '''
    adjmatrix1, arch1 = generate_fully_connected_graph(m, n, connection_probability)
    adjmatrix2, arch2 = generate_fully_connected_graph(m, n, connection_probability)
    matrix = [[0 for i in range(2*m + 2*n)] for j in range(2*m + 2*n)]
    # changes in routers ids
    for i in range(m):
        for j in range(m):
            matrix[i][j] = adjmatrix1[i][j]
            matrix[i+m][j+m] = adjmatrix2[i][j]
    #routers that connect 2 networks
    matrix[0][m] = 1
    matrix[m][0] = 1
    matrix[1][m+1] = 1
    matrix[m+1][1] = 1
    # connections between routers and endpoints
    for i in range(n):
        for j in range(m):
            matrix[i+2*m][j] = adjmatrix1[i+m][j]
            matrix[j][i+2*m] = adjmatrix1[i+m][j]

            matrix[i+2*m+n][j+m] = adjmatrix2[i+m][j]
            matrix[j+m][i+2*m+n] = adjmatrix2[i+m][j]
    arch = {
        'routers': [],
        'endpoints': []
    }
    #create arch
    for i in range(2*m):
        arch['routers'].append({'id': i, 'transmission_capacity':  random.choice([5, 10, 15])})
    for i in range(2*n):
        for j in range(2*m):
            if matrix[i+2*m][j] == 1:
                arch['endpoints'].append({'id': i+2*m, 'gate_id': j})

    return matrix, arch


def fully_connected(adjmatrix: np.ndarray, endpoint_ids: List[int]) -> bool:
    def dfs(adjmatrix: np.ndarray, start_vertex: ID, end_vertex: ID, path: List[ID], visited: List[ID]):
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
    for start_vertex in range(len(adjmatrix)):
        for end_vertex in range(len(adjmatrix)):
            path = dfs(adjmatrix, start_vertex, end_vertex, [], [])
            if path is None:
                raise ValueError('Network is not connected')
    return True

def generate_fully_connected_graph(m:int, n:int, connection_probability:float):
    while True:
        adjmatrix, arch = generate_random_adjacency_matrix(m, n, connection_probability)
        endpoint_ids = []
        for endpoint in arch['endpoints']:
            endpoint_ids.append(endpoint['id'])
        try:
            if fully_connected(adjmatrix, endpoint_ids):
                return adjmatrix, arch
        except:
            pass
        
def generate_random_schedule(arch: Dict, num_of_packages: int, timespan: int = 5):
    endpoint_ids = []
    for endpoint in arch['endpoints']:
        endpoint_ids.append(endpoint['id'])
    schedule = {}
    for i in range(num_of_packages):
        start_id = random.choice(endpoint_ids)
        end_id = random.choice(endpoint_ids)
        while start_id == end_id:
            start_id = random.choice(endpoint_ids)
            end_id = random.choice(endpoint_ids)
        if start_id not in schedule:
            schedule[start_id] = []
        schedule[start_id].append({'destination_id': end_id, 'request_time': random.randrange(1, timespan), 'priority': random.randrange(1,4)})
    return schedule
