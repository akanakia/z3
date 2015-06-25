# -*- coding: utf-8 -*-
"""
Created on Tue Jun 09 16:19:26 2015

@author: Anshul
"""

from z3 import *


class TASolver:
    
    # Constants
    n = 4; # Number of agents
    t = 3;  # Number of targets
    
    # Decision variables
    x = [[Int('x(%d,%d)'%(i,j)) for j in range(t)] for i in range(n)]
    w = [Int('w(%d)'%(j)) for j in range(t)]
    k = [2 for _ in range(t)]
    
    # Set up model
    sol = Solver()
    
    # Agent assignment constraints
    for i in range(n):
        for j in range(t):
            sol.add(Or(x[i][j]==0, x[i][j]==1))
        sol.add(sum(x[i]) <= 1)
    
    sol.add(*[x[agent_id][trgt_id] for (agent_id,trgt_id) in cst])
            
    # Target welfare constraints
    for j in range(t):
        sol.add(Or(w[j]==0, And(sum([r[j] for r in x])>=k[j], w[j]==1)))    
    
    # Add a backtracking point
    sol.push()
    
    # Objective maximization constraint to binary search over
    sol.add(sum(w)==3)
    print(sol.check())
    
    sol.pop()
    sol.add(sum(w)==2)
    
    # Only uncomment new line if you want to see ALL the constraints entered into 
    # the model.
    # print(sol.assertions())
    
    print(sol.check())
    print(sol.model())