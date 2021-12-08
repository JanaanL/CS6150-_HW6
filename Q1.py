import numpy as np
from mip import Model, xsum, minimize, BINARY, OptimizationStatus

"""
Integer Linear Program Solver for Set Cover Problem
"""

#check solution
def check_solution(n, m, S):
    check = np.zeros(m)
    for subset in S:
        for skill in subset:
            check[skill] += 1

    if np.count_nonzero(check) < 500:
        print("The number of skills not covered is ", m - np.count_nonzero(check))
        print("Skills not covered: ", np.where(check==0)[0])
    else:
        print("All skills are covered")


# n = number of people, m = number of skills to cover, d = size of each skill set
n,m,d = 500, 500, 25

#create subsets of skills
S = [None for _ in range(n)]
for i in range(n):
    S[i] = np.random.choice(range(m), d, replace=False)

#check that all skills are covered by at least one person
check_solution(n, m, S)

#create reverse mapping of skills to subsets
V = [set() for _ in range(m)]
for i in range(n):
    for skill in S[i]:
        V[skill].add(i)

#Integer Linear program
model = Model()
#x = [model.add_var(var_type=BINARY) for i in range(n)]
x = [model.add_var(lb=0,ub=1) for i in range(n)]

#objective function: minimize the number of sets
model.objective = minimize(xsum(x[i] for i in range(n)))

#constraint:  make sure every skill is covered at least once
for v in V:
    model += xsum(x[i] for i in v) >= 1

status = model.optimize(max_seconds=300)

if status == OptimizationStatus.OPTIMAL:
    print('optimal solution cost found {}'.format(model.objective_value))
elif status == OptimizationStatus.FEASIBLE:
    print('feasible solution found {}, best possible solution {}'.format(model.objective_value, model.objective_bound))
elif status == OptimizationStatus.NO_SOLUTION_FOUND:
    print('no feasible solution found, lower bound is: {}'.format(model.objective_bound))
if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
    print('solution:')
    for v in model.vars:
#       if abs(v.x) > 1e-6: # only printing non-zeros
        print('{} : {}'.format(v.name, v.x))

#Randomized Rounding of solution
probs = np.zeros(n)
for i in range(n):
    probs[i] = x[i].x

T = [1,2,4,8]
for t in T:
    print("The t value is ", t)

    solution = np.zeros(n)
    for i in range(n):
        prob = np.minimum(1,probs[i]*t)
        #print(prob)
        solution[i] = np.random.choice([0,1],p=[1-prob,prob])
    
    print("The total number of people hired is ", np.count_nonzero(solution))

    #Check Solution
    check = np.zeros(m)
    for i in range(n):
        if solution[i] == 1:
            for skill in S[i]:
                check[skill] += 1
    

    if np.count_nonzero(check) < 500:
        print("The number of skills not covered is ", m - np.count_nonzero(check))
    else:
        print("All skills are covered")

