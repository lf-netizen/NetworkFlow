import matplotlib.pyplot as plt
from itertools import compress
import time

from simulated_annealing import OptimizationModel
from model import *
from network import Network


# INSTRUKCJA
# Parametr który się zmienia w kolejnych iteracjach wrzucamy w listę. Pozostałe (które są stałe) jako floaty. 

# bazowe parametry:
# t0 = 10e5
# t1 = 10e-3
# alpha = 0.95
# epoch_size = 50

t0 = 10e5
t1 = 10e-3
alpha = [0.98, 0.95, 0.9, 0.8, 0.5, 0.1]
epoch_size = 50

nbhoods_active = [1, 1, 1, 1, 1, 1]

# for plotting
nrows = 2
ncols = 3

model_names = ('Dense model', 'Sparse model', 'Mean model')
# NAZWA PARAMETRU /ALPHA/T0T1/EPOCHSIZE/ i current_params[?] DO ZMIANY: LINIA 66, 63, 76
#####
params = [t0, t1, alpha, epoch_size]
# change params to list for convinience
for param in params:
    if isinstance(param, list):
        num_tests = len(param)

assert num_tests == nrows*ncols

for it, param in enumerate(params):
    if not isinstance(param, list):
        params[it] = [param] * nrows*ncols

for it_model, model_loader in enumerate([dense_model_predefined, sparse_model_predefined, mean_model_predefined]):
    adjmatrix, arch, schedule = model_loader()
    network = Network(arch)
    network.load_schedule(schedule)
    model = OptimizationModel(network, adjmatrix)

    nbhoods = [model.change_solution, model.change_solution2, model.change_solution3, model.change_solution4, model.change_solution5, model.change_solution6]
    nbhoods = set(compress(nbhoods, nbhoods_active))
    
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=(5*ncols, 5*nrows), sharey=True)
    fig.suptitle(f'{model_names[it_model]}')

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print('=============================')
    print(model_names[it_model])
    print(f'Started {current_time} CET')
    print('t0|t1|min|max|iterations|improvements|deteriorations')
    print('=============================')
    for it_row in range(nrows):
        for it_col in range(ncols):
            curr_params = [param[it_row*ncols+it_col] for param in params]
            _, iterations, cost_array = model.run_model(*curr_params, neighbourhoods_active=nbhoods)
            model.network.reset_state(with_schedule=False)
            
            title = f't0 = {curr_params[0]:.0E}, t1 = {curr_params[1]:.0E}'
            axs[it_row, it_col].plot(cost_array)
            axs[it_row, it_col].grid()
            axs[it_row, it_col].set_title(title)
            axs[it_row, it_col].set_xlabel('iterations')
            axs[it_row, it_col].set_ylabel('loss')
            
            logs = [curr_params[0], curr_params[1], min(cost_array), max(cost_array), len(cost_array), sum(prev > next for prev, next in zip(cost_array[:-1], cost_array[1:])), sum(prev < next for prev, next in zip(cost_array[:-1], cost_array[1:]))]
            print(' '.join([str(num) for num in logs]))
    
    plt.savefig(f'charts/t0t1_{model_names[it_model].replace(" ", "_").lower()}.png', bbox_inches='tight')
    model.network.reset_state(with_devices=True)
