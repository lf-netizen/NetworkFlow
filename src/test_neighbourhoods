import matplotlib.pyplot as plt
from itertools import compress
import time

from simulated_annealing import OptimizationModel
from model import *
from network import Network


# INSTRUKCJA
# neighbourhoods selection in lines 41-42
# !!!!! check if params are correct !!!!!! 

# bazowe parametry:
# t0 = 10e5
# t1 = 10e-3
# alpha = 0.95
# epoch_size = 50

t0 = 10e5
t1 = 10e-3
alpha = 0.95
epoch_size = 50

nbhoods_active = [1, 1, 1, 1, 1, 1]

# for plotting
nrows = 1
ncols = 3

with open('logs/test_neighbourhoods.txt', 'w') as file:
    model_names = ('Dense model', 'Sparse model', 'Mean model')
    # NAZWA PARAMETRU /ALPHA/T0T1/EPOCHSIZE/ i current_params[?] DO ZMIANY: LINIA 66, 63, 76
    #####
    params = [t0, t1, alpha, epoch_size]
    file.write('min|max|iterations|improvements|deteriorations')
    for it, param in enumerate(params):
        if not isinstance(param, list):
            params[it] = [param] * nrows*ncols

    for i in range(2):
        if i==0:
            nbhoods_active = [0, 0, 0, 1, 0, 0]
        if i==1:
            nbhoods_active = [0, 0, 0, 0, 1, 0]
        file.write(f'nbhood active: {nbhoods_active}\n')

        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(5*ncols, 5*nrows), sharey=True)
            
        for it_model, model_loader in enumerate([dense_model_predefined, sparse_model_predefined, mean_model_predefined]):
            adjmatrix, arch, schedule = model_loader()
            network = Network(arch)
            network.load_schedule(schedule)
            model = OptimizationModel(network, adjmatrix)

            nbhoods = [model.change_solution, model.change_solution2, model.change_solution3, model.change_solution4, model.change_solution5, model.change_solution6]
            nbhoods = set(compress(nbhoods, nbhoods_active))
            
            fig.suptitle(f'active neighbourhoods: {nbhoods_active}')

            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print('=============================')
            file.write(model_names[it_model])
            file.write('\n')
            print(model_names[it_model])
            print(f'Started {current_time} CET')
            print('min|max|iterations|improvements|deteriorations')
            print('=============================')
            curr_params = [param[it_model] for param in params]
            _, iterations, cost_array = model.run_model(*curr_params, neighbourhoods_active=nbhoods)
            model.network.reset_state(with_schedule=False)
            
            title = f'{model_names[it_model]}'
            axs[it_model].plot(cost_array)
            axs[it_model].grid()
            axs[it_model].set_title(title)
            axs[it_model].set_xlabel('iterations')
            axs[it_model].set_ylabel('loss')
            
            logs = [min(cost_array), max(cost_array), len(cost_array), sum(prev > next for prev, next in zip(cost_array[:-1], cost_array[1:])), sum(prev < next for prev, next in zip(cost_array[:-1], cost_array[1:]))]
            print(' '.join([str(num) for num in logs]))
            file.write(' '.join([str(num) for num in logs]))
            file.write('\n')
            model.network.reset_state(with_devices=True)
            
        plt.savefig(f'charts/nbhood_{i}{model_names[it_model].replace(" ", "_").lower()}.png', bbox_inches='tight')
        


# from itertools import compress
# import time

# from network import Network
# from simulated_annealing import OptimizationModel   
# from model import dense_model_predefined, mean_model_predefined, sparse_model_predefined

# ### 
# iterations = 100
# ### default params
# t0 = 10e5
# t1 = 10e-3
# alpha = 0.95
# epoch_size = 50
# nbhoods_active = [1, 1, 1, 1, 1, 1]
# ###

# with open('logs/test_100x_repeat.txt', 'w') as file:
#     for iter in range(iterations):
#         t = time.localtime()
#         current_time = time.strftime("%H:%M:%S", t)
#         print(f'Iter {iter}; {current_time} CET')
#         for it_model, model_loader in enumerate([dense_model_predefined, sparse_model_predefined, mean_model_predefined]):
            
#             file.write(f'MODEL {it_model}\n')

#             adjmatrix, arch, schedule = model_loader()
#             network = Network(arch)
#             network.load_schedule(schedule)
#             model = OptimizationModel(network, adjmatrix)

#             nbhoods = [model.change_solution, model.change_solution2, model.change_solution3, model.change_solution4, model.change_solution5, model.change_solution6]
#             nbhoods = set(compress(nbhoods, nbhoods_active))

#             time_start = time.perf_counter()
#             _, _, cost_array = model.run_model(t0, t1, alpha, epoch_size, neighbourhoods_active=nbhoods)
#             time_stop = time.perf_counter()
            
#             file.write(f'{(time_stop - time_start):.3f} s; {cost_array}\n')
            
#             model.network.reset_state(with_devices=True)
    