from itertools import compress
import time

from network import Network
from simulated_annealing import OptimizationModel   
from model import dense_model_predefined, sparse_model_predefined, mean_model_predefined
from test import generate_random_schedule

### 
iterations = 5
package_counts = [10**i for i in range(1, 6)] # from 10 to million
### default params
t0 = 10e5
t1 = 10e-3
alpha = 0.95
epoch_size = 50
nbhoods_active = [1, 1, 1, 1, 1, 1]
###

with open('logs/test_packages_count.txt', 'w') as file:
    for it_model, model_loader in enumerate((dense_model_predefined, sparse_model_predefined, mean_model_predefined)):
        print(f'================\nMODEL {it_model}: {current_time} CET')
        
        file.write(f'MODEL {it_model}\n')

        adjmatrix, arch, _ = model_loader()
        network = Network(arch)
        model = OptimizationModel(network, adjmatrix)

        nbhoods = [model.change_solution, model.change_solution2, model.change_solution3, model.change_solution4, model.change_solution5, model.change_solution6]
        nbhoods = set(compress(nbhoods, nbhoods_active))
        
        for package_count in package_counts:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print(f'Started {package_count} {current_time} CET\n')
            file.write(f'PACKAGE COUNT: {package_count}\n')
            for iter in range(iterations):
                schedule = generate_random_schedule(arch, package_count)
                model.network.load_schedule(schedule)

                time_start = time.perf_counter()
                _, _, cost_array = model.run_model(t0, t1, alpha, epoch_size, nbhoods)
                time_stop = time.perf_counter()

                file.write(f'{(time_stop - time_start):.3f} s; {cost_array}\n')
                
                model.network.reset_state(with_schedule=True)

        model.network.reset_state(with_devices=True)
