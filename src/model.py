from custom_types import ID
from test import generate_random_schedule, generate_mean_case,generate_fully_connected_graph, generate_random_adjacency_matrix
import numpy as np
import pickle
import json

# for generate random network in GUI -> GraphFrame
def random_network_model(number_of_routers, number_of_PCs, number_of_packages, connection_probability, timespan):
    adjmatrix, arch = generate_random_adjacency_matrix(m=number_of_routers, n=number_of_PCs, connection_probability=0.4)
    schedule = generate_random_schedule(arch=arch, num_of_packages=number_of_packages)
    return adjmatrix, arch, schedule

def dense_test_model():
    adjmatrix, arch = generate_fully_connected_graph(m=40,n=20,connection_probability=0.8)
    schedule = generate_random_schedule(arch=arch,num_of_packages=1000)
    return adjmatrix, arch, schedule

def sparse_test_model():
    adjmatrix, arch = generate_fully_connected_graph(m=40,n=20,connection_probability=0.2)
    schedule = generate_random_schedule(arch=arch,num_of_packages=1000)
    return adjmatrix, arch, schedule

def mean_test_model():
    adjmatrix, arch = generate_mean_case(m=20,n=10,connection_probability=0.4)
    schedule = generate_random_schedule(arch=arch,num_of_packages=1000)
    return adjmatrix, arch, schedule

def model1():
    adjmatrix = np.array([[0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0],
                        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
                        [1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
                        [1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
                        [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
                        [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
                        [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
                        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]],dtype=object)
    arch = {
        'routers': [
            {'id': 0, 'transmission_capacity':  5},
            {'id': 1, 'transmission_capacity': 10},
            {'id': 2, 'transmission_capacity': 10},
            {'id': 3, 'transmission_capacity': 5},
            {'id': 4, 'transmission_capacity': 10},
            {'id': 5, 'transmission_capacity': 10},
            {'id': 6, 'transmission_capacity': 5}
        ],
        'endpoints': [
            {'id': 7, 'gate_id': 0},
            {'id': 8, 'gate_id': 1},
            {'id': 9, 'gate_id': 2},
            {'id': 10, 'gate_id': 3}
        ]
    }
    schedule = {
        7: [
            {'destination_id': 8,      'request_time': 2, 'priority': 2},
            {'destination_id': [9, 10], 'request_time': 4, 'priority': 2},
            {'destination_id': 9,      'request_time': 3, 'priority': 1}
        ],
        8: [
            {'destination_id': 7,      'request_time': 1, 'priority': 2},
            {'destination_id': 9, 'request_time': 2, 'priority': 2},
            {'destination_id': 10,      'request_time': 3, 'priority': 1}
        ],
        9: [
            {'destination_id': 7, 'request_time': 5, 'priority': 2},
            {'destination_id': 8, 'request_time': 3, 'priority': 1}
        ],
        10: [
            {'destination_id': 7, 'request_time': 4, 'priority': 2},
            {'destination_id': 8, 'request_time': 6, 'priority': 2},
            {'destination_id': 9, 'request_time': 3, 'priority': 1}
        ]
    }

    # example pipeline
    return adjmatrix, arch, schedule
    # network = Network(arch)
    # network.load_schedule(schedule)
    # return OptimizationModel(network=network, adjmatrix=adjmatrix)

def model2():
    # simple model
    adjmatrix = np.array([[0, 1, 1, 1, 1, 0, 0, 0],
                          [1, 0, 1, 1, 0, 1, 0, 0],
                          [1, 1, 0, 1, 0, 0, 1, 0],
                          [1, 1, 1, 0, 0, 0, 0, 1],
                          [1, 0, 0, 0, 0, 0, 0, 0],
                          [0, 1, 0, 0, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0, 0]],dtype=object)
    arch = {
        'routers': [
            {'id': 0, 'transmission_capacity': 3},
            {'id': 1, 'transmission_capacity': 3},
            {'id': 2, 'transmission_capacity': 3},
            {'id': 3, 'transmission_capacity': 3},
        ],
        'endpoints': [
            {'id': 4, 'gate_id': 0},
            {'id': 5, 'gate_id': 1},
            {'id': 6, 'gate_id': 2},
            {'id': 7, 'gate_id': 3}
        ]
    }
    schedule = {
        4: [
            {'destination_id': 5, 'request_time': 1, 'priority': 1},
            {'destination_id': 6, 'request_time': 1, 'priority': 1},
            {'destination_id': 7, 'request_time': 1, 'priority': 1}
        ],
        5: [
            {'destination_id': 4, 'request_time': 1, 'priority': 1},
            {'destination_id': 6, 'request_time': 1, 'priority': 1},
            {'destination_id': 7, 'request_time': 1, 'priority': 1}
        ],
        6: [
            {'destination_id': 4,'request_time': 1, 'priority': 1},
            {'destination_id': 5,'request_time': 1, 'priority': 1},
            {'destination_id': 7,'request_time': 1, 'priority': 1}
        ],
        7: [
            {'destination_id': 4, 'request_time': 1, 'priority': 1},
            {'destination_id': 5, 'request_time': 1, 'priority': 1},
            {'destination_id': 6, 'request_time': 1, 'priority': 1}
        ]
    }

    # example pipeline

    return adjmatrix, arch, schedule

def model3():
    adjmatrix = np.array([[0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0],
                    [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0],
                    [1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
                    [1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1],
                    [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
                    [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]],dtype=object)
    arch = {
        'routers': [
            {'id': 0, 'transmission_capacity':  5},
            {'id': 1, 'transmission_capacity': 10},
            {'id': 2, 'transmission_capacity': 10},
            {'id': 3, 'transmission_capacity': 5},
            {'id': 4, 'transmission_capacity': 10},
            {'id': 5, 'transmission_capacity': 10},
            {'id': 6, 'transmission_capacity': 5}
        ],
        'endpoints': [
            {'id': 7, 'gate_id': 0},
            {'id': 8, 'gate_id': 1},
            {'id': 9, 'gate_id': 2},
            {'id': 10, 'gate_id': 3}
        ]
    }
    schedule = {
        7: [
            {'destination_id': 8,      'request_time': 2, 'priority': 2},
            {'destination_id': [9, 10], 'request_time': 4, 'priority': 2},
            {'destination_id': 9,      'request_time': 3, 'priority': 1}
        ],
        8: [
            {'destination_id': 7,      'request_time': 1, 'priority': 2},
            {'destination_id': 9, 'request_time': 2, 'priority': 2},
            {'destination_id': 10,      'request_time': 3, 'priority': 1}
        ],
        9: [
            {'destination_id': 7, 'request_time': 5, 'priority': 2},
            {'destination_id': 8, 'request_time': 3, 'priority': 1}
        ],
        10: [
            {'destination_id': 7, 'request_time': 4, 'priority': 2},
            {'destination_id': 8, 'request_time': 6, 'priority': 2},
            {'destination_id': 9, 'request_time': 3, 'priority': 1}
        ]
    }

    # example pipeline

    return adjmatrix, arch, schedule


def unpack_json(json_data: str):
    # Deserialize the JSON data to a Python list
    model_data = json.loads(json_data)
    model_data['schedule'] = {int(k): v for k, v in model_data['schedule'].items()}
    return np.array(model_data['adjmatrix']), model_data['arch'], model_data['schedule']

def model_from_file(name) -> callable:
    def loader():
        # Load the JSON data from the file
        with open(f"models/{name}.json", "r") as json_file:
            json_data = json_file.read()
        
        return unpack_json(json_data)
    return loader

def model_save(name, adjmatrix, arch, schedule):
    model_data = {
        'adjmatrix': adjmatrix if isinstance(adjmatrix, list) else adjmatrix.tolist(),
        'arch': arch,
        'schedule': schedule
    }
    json_model = json.dumps(model_data)
    with open(f"models/{name}.json", "w") as json_file:
        json_file.write(json_model)


def dense_model_predefined():
    return model_from_file('predefined_dense')()

def sparse_model_predefined():
    return model_from_file('predefined_sparse')()

def mean_model_predefined():
    return model_from_file('predefined_mean')()
    

if __name__ == "__main__":
    pass
    # adjmatrix, arch, schedule = mean_test_model()
    # model_data = {
    #     'adjmatrix': adjmatrix,
    #     'arch': arch,
    #     'schedule': schedule
    # }

    # model_save('predefined_dense', *dense_model_predefined())
    # model_save('predefined_sparse', *sparse_model_predefined())
    # print(model_load('predefined_dense'))
    
    # adjmatrix, arch, schedule = model2()
    # model_save('simple', adjmatrix, arch, schedule)

    
        