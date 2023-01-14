from itertools import compress
import time

from network import Network
from simulated_annealing import OptimizationModel   
from test import generate_random_schedule, generate_mean_case,generate_fully_connected_graph

### 
iterations = 5
network_sizes = [10, 20, 30, 40, 50, 60, 70, 80] # number of routers in the network, PCs are half as much
### default params
t0 = 10e5
t1 = 10e-3
alpha = 0.95
epoch_size = 50
nbhoods_active = [1, 1, 1, 1, 1, 1]
###

with open('logs/test_network_size.txt', 'w') as file:
    for network_size in network_sizes:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(f'size {network_size} started {current_time} CET')
   
        file.write(f'============\nnetwork size: {network_size}\n============\n')

        adjmatrix, arch = generate_fully_connected_graph(m=network_size,n=network_size//2,connection_probability=0.8)
        network = Network(arch)
        model = OptimizationModel(network, adjmatrix)

        nbhoods = [model.change_solution, model.change_solution2, model.change_solution3, model.change_solution4, model.change_solution5, model.change_solution6]
        nbhoods = set(compress(nbhoods, nbhoods_active))

        for iter in range(iterations):
            schedule = generate_random_schedule(arch=arch, num_of_packages=25*network_size)
            network.load_schedule(schedule)


            time_start = time.perf_counter()
            _, _, cost_array = model.run_model(t0, t1, alpha, epoch_size, nbhoods)
            time_stop = time.perf_counter()

            file.write(f'{(time_stop - time_start):.3f} s; {cost_array}\n')

            model.network.reset_state(with_schedule=True)
        model.network.reset_state(with_devices=True)
    

        
