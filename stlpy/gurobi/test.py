import gurobipy as gp
from gurobipy import GRB
import cvxpy as cp
import os
import yaml
from stlpy.STL.sos1 import addsos1constraint
from gray import GrayCode
import numpy as np
import math

# a = cp.Variable(12)
# cons = []
# cons += [a <= 2]
# cons += [a >= 1]
# cons += [sum(a)<=12]
# cost = sum(a)
nz = 8
lambd, y, cons = addsos1constraint(nz)
# lambd = cp.Variable(nz)
# a = GrayCode()
# num_y = math.ceil(math.log2(nz))
# X = a.getGray(num_y)
# Xlist = []
# for i in range(2 ** num_y):
#     Xlist += X[i]
# Xarr = list(map(int, Xlist))
# num_row = int(len(Xarr) / num_y)
# Mat = np.array(Xarr).reshape(num_row, num_y)
# binary_encoding = Mat[:nz, :]
# y = cp.Variable(num_y, boolean=True)
# cons = []
# for i in range(nz):
#     cons += [lambd[i] >= 0]
# cons += [sum(lambd) == 1]
#
# for j in range(0, num_y):
#     lambda_sum1 = 0
#     lambda_sum2 = 0
#     for k in range(0, nz):
#         if binary_encoding[k, j] == 1:
#             lambda_sum1 += lambd[k]
#         elif binary_encoding[k, j] == 0:
#             lambda_sum2 += lambd[k]
#         else:
#             print("Runtime_error: The binary_encoding entry can be only 0 or 1.")
#             break
#     cons += [lambda_sum1 <= y[j]]
#     cons += [lambda_sum2 <= 1 - y[j]]
#
cons += [lambd[-1] ==1]
cost = sum(y)
prob = cp.Problem(cp.Minimize(cost), cons)

solver = cp.GUROBI

grb_param_dict = {}
with open('/MPC\config\mosek.yaml') as file:
    grb_param_dict = yaml.load(file, Loader=yaml.FullLoader)
    prob.solve(solver=solver, **grb_param_dict, verbose=True)

if prob.status in ['optimal', 'optimal_inaccurate'] and prob.status not in ['infeasible','unbounded']:
    print('true')
    print(y.value)
    print(lambd.value)



