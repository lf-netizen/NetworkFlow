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

for it_model, model_loader in enumerate([dense_model_predefined, sparse_model_predefined, mean_model_predefined]):
    adjmatrix, arch, schedule = model_loader()
    network = Network(arch)
    network.load_schedule(schedule)
    model = OptimizationModel(network, adjmatrix)

    nbhoods = [model.change_solution, model.change_solution2, model.change_solution3, model.change_solution4, model.change_solution5, model.change_solution6]
    nbhoods = set(compress(nbhoods, nbhoods_active))

    for iter in range(iterations):
        time_start = time.perf_counter()
        _, _, cost_array = model.run_model(t0, t1, alpha, epoch_size, neighbourhoods_active=nbhoods)
        time_stop = time.perf_counter()
        print(len(cost_array))
        model.network.reset_state(with_schedule=False)
        print(f'{(time_stop - time_start)*1000:.0f}')
    
    model.network.reset_state(with_devices=True)
    

        
