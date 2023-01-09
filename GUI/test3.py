import copy

dic = {1: {1,2}, 2: {4}}
d = {}
d = copy.deepcopy(dic)
dic = {1: {}, 2: {}}

print(d)
print(dic)