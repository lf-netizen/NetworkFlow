import matplotlib.pyplot as plt
from itertools import compress

from simulated_annealing import OptimizationModel
from model import *
from network import Network


# INSTRUKCJA
# Parametr który się zmienia w kolejnych iteracjach wrzucamy w listę. Pozostałe (które są stałe) jako floaty. 
# num_tests odpowiada ilości testów tj. jest równy długości tej listy (albo dowolnie, kiedy chcemy testować sąsiedztwa). 

num_tests = 3

t0 = 10e3
t1 = 10e-1
alpha = [0.95, 0.9, 0.7]
epoch_size = 10

nbhoods_active = [1, 1, 1, 1, 1, 1]

######
params = [t0, t1, alpha, epoch_size]
# change params to list for convinience
for param in params:
    if isinstance(param, list):
        num_tests = len(param)

for it, param in enumerate(params):
    if not isinstance(param, list):
        params[it] = [param] * num_tests

for it_model, model in enumerate([model1, model2, model3]):
    adjmatrix, arch, schedule = model()
    network = Network(arch)
    network.load_schedule(schedule)
    model = OptimizationModel(network, adjmatrix)

    nbhoods = [model.change_solution, model.change_solution2, model.change_solution3, model.change_solution4, model.change_solution5, model.change_solution6]
    nbhoods = set(compress(nbhoods, nbhoods_active))
    
    fig, axs = plt.subplots(nrows=1, ncols=num_tests, figsize=(5*num_tests, 5), sharey=True)
    fig.suptitle(f'Model {it_model+1}; nbhoods_active={nbhoods_active}')

    for it in range(num_tests):
        plt.subplot(1, num_tests, it+1)
        plt.grid()
        curr_params = [param[it] for param in params]
        plt.title('t0 = {}, t1 = {}, al = {}, e_s = {}'.format(*curr_params))
        plt.xlabel('iterations')
        plt.ylabel('loss')
        _, iterations, cost_array = model.run_model(*curr_params, neighbourhoods_active=nbhoods)
        model.network.reset_state(with_schedule=False)
        axs[it].plot(cost_array)
    
    plt.show()
    model.network.reset_state(with_devices=True)
