# -*- coding: utf-8 -*-
"""
Created on Tue Jun 09 16:19:26 2015

@author: Anshul
"""

from z3 import *


# Constants
n = 4; # Number of agents
t = 3;  # Number of targets

# Decision variables
x = [[Int('x(%d,%d)'%(i,j)) for j in range(t)] for i in range(n)]

# Set up model
sol = Solver()


for i in range(n):
    for j in range(t):
        sol.add(Or(x[i][j]==0, x[i][j]==1))
    sol.add(sum(x[i]) <= 1)
        


# Agent constraints
sol.add(x[0][2]==0, x[1][0]==0, x[2][2]==0, x[3][0]==0)

print(sol.check())
print(sol.model())