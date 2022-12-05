import numpy as np
import copy

def create_random_solution(m:int, n:int, G:np.ndarray) -> np.ndarray:

    '''
    Creates a random matrix representing a legal and acyclic connection between servers and PC's
    
    inputs: 
    m - number of reveivers
    n - number of routers
    G - adjacency matrix showing connections between routers and PC's

    outputs:
    cadidate solution - np.ndarray of size (m, n+m)
    '''
    while(True):
        #flag value equal to 0 if we found out an illegal solution
        flag = 1
        candidate_solution = np.random.randint(0,n+m,(m,n+m))
        for row in candidate_solution:
            for col,val in enumerate(row):
                if(G[col][val] == 0):
                    flag = 0
                    break
            if flag == 0:
                break
        if is_acyclic(candidate_solution,G) and flag == 1:
            return candidate_solution


def is_acyclic(current_solution:np.ndarray,G:np.ndarray) -> bool:
    '''
    Checks if current solution is acyclic
    
    inputs: 
    current_solution - current best solution for the algorithm
    G - adjacency matrix showing connections between routers and PC's

    outputs:
    bool value - true if no cycles were found
    '''

    m = current_solution.shape[0]
    n = current_solution.shape[1] - current_solution.shape[0]
    #checking all possible connections between PC's 
    for target_pc_index, row in enumerate(current_solution,start = n):
        for starting_pc_index in range(n,n+m):
            current_index = starting_pc_index
            visited = [current_index]
            #check if current router was added to visited array until we reach the target index
            while(current_index != target_pc_index):
                next_index = row[current_index]
                if(next_index in visited):
                    return False
                else:
                    current_index = next_index
                    visited.append(next_index)
    return True




def change_solution(current_solution:np.ndarray, G:np.ndarray) -> np.ndarray:
    '''
    Changes random value in the current_solution matrix and checks if this solution is possible

    inputs: 
    current_solution - current best solution for the algorithm
    G - adjacency matrix showing connections between routers and PC's

    outputs:
    current_solution - new_solution
    '''

    n = current_solution.shape[1] - current_solution.shape[0]
    x,y = np.random.randint(0,current_solution.shape[0]),np.random.randint(0,current_solution.shape[1])
    current_solution_copy = copy.deepcopy(current_solution)

    #ToDo: What if there are no legal neighbours
    while(True):
        new_directory = np.random.randint(0,n)
        #checking if there is connection between router y and new directory
        if G[y][new_directory] == 1:
            #checking if new solution is acyclic
            current_solution_copy[x,y] = new_directory
            if is_acyclic(current_solution_copy,G):
                current_solution[x,y] = new_directory
                return current_solution


def simulated_annealing(loss_fun:callable, m:int, n:int, G:np.ndarray, t:np.array, T0:float = 0.95, T1:float = 0.001, alpha:float = 0.5, epoch_size:int = 10):
    '''
    Minimizes loss function using simulated annealing

    inputs:
    m - number of reveivers
    n - number of routers
    G - adjacency matrix showing connections between routers
    t - array of length n containing cost related to using a particular router in the path
    T0 - starting temperature in the simulated annealing algorithm
    T1 - temperature at which the algorithm stops
    alpha - paramter used to change T after every iteration

    outputs:
    x - solution: np.ndarray of shape(m,n+m) where values represent indices of routers to which packages should be sent, 
    rows represent the target reveiver and column represents index of current server/PC where the package is
    cost - array representing loss_function values at every iteration
    '''
    #creating a random solution
    x = create_random_solution(m,n,G)
    cost = []
    T = T0
    while(T1 < T):
        for _ in range(epoch_size):
            x1 = change_solution(x,G)
            if loss_fun(x1,t) < loss_fun(x,t):
                x = x1
            else:
                probability = np.exp((loss_fun(x1,t) - loss_fun(x,t))/T)
                if probability > np.random.random():
                    x = x1
            cost.append(x)
        T = T * alpha
    return x, cost


# n = 3
# m = 4
# G = np.array([[1,1,1,1,1,1,1],
#                 [1,1,1,1,1,1,1],
#                 [1,1,1,1,1,1,1],
#                 [1,1,1,0,0,0,0],
#                 [1,1,1,0,0,0,0],
#                 [1,1,1,0,0,0,0],
#                 [1,1,1,1,0,0,0]],dtype=object)
# current_solution = np.array([[1,2,3,3,0,0,0],
#                              [2,0,4,1,4,1,1],
#                              [5,5,0,2,2,5,2],
#                              [6,6,1,2,2,2,6]],dtype=object)
# print(is_acyclic(current_solution,G))
# print(create_random_solution(m,n,G))


