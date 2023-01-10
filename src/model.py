from custom_types import ID
from test import generate_random_schedule, generate_mean_case,generate_fully_connected_graph
import numpy as np

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
            {'id': 0, 'transmission_capacity':  5},
            {'id': 1, 'transmission_capacity': 10},
            {'id': 2, 'transmission_capacity': 10},
            {'id': 3, 'transmission_capacity': 5},
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
            {'destination_id': 5,      'request_time': 2, 'priority': 2},
            {'destination_id': 6, 'request_time': 4, 'priority': 2},
            {'destination_id': 7,      'request_time': 3, 'priority': 1}
        ],
        5: [
            {'destination_id': 4,      'request_time': 1, 'priority': 2},
            {'destination_id': 6, 'request_time': 2, 'priority': 2},
            {'destination_id': 7,      'request_time': 3, 'priority': 1}
        ],
        6: [
            {'destination_id': 4, 'request_time': 5, 'priority': 2},
            {'destination_id': 5, 'request_time': 3, 'priority': 1},
            {'destination_id': 7, 'request_time': 3, 'priority': 1}
        ],
        7: [
            {'destination_id': 4, 'request_time': 4, 'priority': 2},
            {'destination_id': 5, 'request_time': 6, 'priority': 2},
            {'destination_id': 6, 'request_time': 3, 'priority': 1}
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


def dense_model_predefined():
    pickle_in = open("models/predefined_dense_model.pkl","rb")
    model_data = pickle.load(pickle_in)
    return model_data['adjmatrix'], model_data['arch'], model_data['schedule']

def sparse_model_predefined():
    pickle_in = open("models/predefined_sparse_model.pkl","rb")
    model_data = pickle.load(pickle_in)
    return model_data['adjmatrix'], model_data['arch'], model_data['schedule']

def mean_model_predefined():
    pickle_in = open("models/predefined_mean_model.pkl","rb")
    model_data = pickle.load(pickle_in)
    return model_data['adjmatrix'], model_data['arch'], model_data['schedule']

if __name__ == "__main__":
    import pickle

    adjmatrix, arch, schedule = mean_test_model()
    model_data = {
        'adjmatrix': adjmatrix,
        'arch': arch,
        'schedule': schedule
    }
    pickle_out = open("models/predefined_mean_model.pkl","wb")
    pickle.dump(model_data, pickle_out)
    pickle_out.close()

        