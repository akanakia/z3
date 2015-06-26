# -*- coding: utf-8 -*-
"""
Created on Tue Jun 09 16:19:26 2015

@author: Anshul
"""

from z3 import *


class TASolver:    
    
    def __init__(self):
        self.set_ta_vars()
        # Z3 model solver
        self._s = Solver() 

    def set_ta_vars(self, n = 1, t = 1, k = [1], cst = [], w = [1]):
        # Set some defaults for user variables
        self.n   = n
        self.t   = t
        self.k   = k
        self.cst = cst    
    
    def solve(self):
        """
        """        
        # Setup initial constraints
        self._init_model()        
        
        # Add a backtracking point
        self._s.push()

        # First check if any valid assignment exists
        self._s.add(sum(self._W)==1)
        res = self._s.check()
        if res != sat:
            print(res)
            print('This system has no valid useful assignments.')
            return
        
        self._s.pop()
        self._s.push()
        
        # Next check if an optimal assignment exists
        self._s.add(sum(self.W)==self.t)        
        # Binary search through possible solutions
        
        
    def _init_model(self):
        """
        Sets up all the decision variables and constraints except the objective
        max. constraints
        """
        # Decision variables
        self._x = [[Int('x(%d,%d)'%(i,j)) for j in range(self.t)] for i in range(self.n)]
        self._W = [Int('w(%d)'%(j)) for j in range(self.t)]

        # Reset the solver        
        self._s.reset()
        
        # Agent assignment constraints
        for i in range(self.n):
            for j in range(self.t):
                self._s.add(Or(self._x[i][j]==0, self._x[i][j]==1))
            self._s.add(sum(self._x[i]) <= 1)
        
        self._s.add(*[self._x[agent_id][trgt_id]==0 for (agent_id,trgt_id) in self.cst])
                
        # Target welfare constraints
        for j in range(self.t):
            self._s.add(Or(self._W[j]==0, And(sum([r[j] for r in self._x])>=self.k[j], self._W[j]==1)))
        