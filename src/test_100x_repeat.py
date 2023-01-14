from itertools import compress
import time

from network import Network
from simulated_annealing import OptimizationModel   
from model import dense_model_predefined, mean_model_predefined, sparse_model_predefined

### 
iterations = 100
### default params
t0 = 10e5
t1 = 10e-3
alpha = 0.95
epoch_size = 50
nbhoods_active = [1, 1, 1, 1, 1, 1]
###

with open('logs/test_100x_repeat.txt', 'w') as file:
    for iter in range(iterations):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(f'Iter {iter}; {current_time} CET')
        for it_model, model_loader in enumerate([dense_model_predefined, sparse_model_predefined, mean_model_predefined]):
            
            file.write(f'MODEL {it_model}\n')

            adjmatrix, arch, schedule = model_loader()
            network = Network(arch)
            network.load_schedule(schedule)
            model = OptimizationModel(network, adjmatrix)

            nbhoods = [model.change_solution, model.change_solution2, model.change_solution3, model.change_solution4, model.change_solution5, model.change_solution6]
            nbhoods = set(compress(nbhoods, nbhoods_active))

            time_start = time.perf_counter()
            _, _, cost_array = model.run_model(t0, t1, alpha, epoch_size, neighbourhoods_active=nbhoods)
            time_stop = time.perf_counter()
            
            file.write(f'{(time_stop - time_start):.3f} s; {cost_array}\n')
            
            model.network.reset_state(with_devices=True)
    

        
