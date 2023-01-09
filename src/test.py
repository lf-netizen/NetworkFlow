import numpy as np
import random
def generate_random_adjacency_matrix(m:int, n:int):
    '''
    m: number of routers
    n: number of computers
    '''
    matrix = [[0 for i in range(m+n)] for j in range(m+n)]
    #connections between routers
    for i in range(m):
        for j in range(m):
            if np.random.random() > 0.5:
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
        gate_id = random.randrange(0,m)
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

    return np.array(matrix, dtype= object), arch

def generate_mean_case(m, n):
    '''
    One network made of 2 network connected by 2 routers
    m: number of routers in one network
    n: number of computers in one network
    '''
    network1 = generate_random_adjacency_matrix(m, n)
    network2 = generate_random_adjacency_matrix(m, n)
    matrix = [[0 for i in range(2*m + 2*n)] for j in range(2*m + 2*n)]
    # changes in routers ids
    for i in range(m):
        for j in range(m):
            matrix[i][j] = network1[i][j]
            matrix[i+m][j+m] = network2[i][j]
    #routers that connect 2 networks
    matrix[0][m] = 1
    matrix[m][0] = 1
    matrix[1][m+1] = 1
    matrix[m+1][1] = 1
    # changes in endpoints ids
    # not finished
    # for i in range(m):
    #     for j in range(n):

print(generate_random_adjacency_matrix(10,5))
