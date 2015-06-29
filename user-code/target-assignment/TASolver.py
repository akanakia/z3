# -*- coding: utf-8 -*-
"""
Created on Tue Jun 09 16:19:26 2015

@author: Anshul
"""

import math
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
        self.w   = w
        
    def show_solution(self):
        if self._s.check() == sat:
            print('Solution:')
            print(self._s.model())        
        
    def solve(self):
        """
        """        
        # Setup initial constraints & add a backtracking point
        self._init_model()        
        self._s.push()

        # First check if any valid assignment exists
        TW_low  = 1
        self._s.add(sum(self._W)>=TW_low, self._TW==sum(self._W))
        if self._s.check() != sat:
            print('This system has no valid useful assignments.')
            return
        
        TW_low = self._s.model()[self._TW].as_long()
        self._s.pop()
        
        # Then check if the maximal assigment is possible        
        self._s.push()
        TW_high = sum(self.w)
        self._s.add(sum(self._W)==TW_high, self._TW==sum(self._W))
        if self._s.check() == sat:
            print('A maximal assignment was found. TW = %d'%self._s.model()[self._TW].as_long())
            return
        
        TW_high -= 1
        self._s.pop()
        
        # Binary search through possible solutions        
        (sat_res, TW_res) = self._binary_search(TW_low, TW_high)
        if sat_res == sat:
            print('An optimal assignment was found. TW = %d'%self._s.model()[self._TW].as_long())
        else:
            print('Something went horribly wrong! This should never happen.')
        
    def _init_model(self):
        """
        Sets up all the decision variables and constraints except the objective
        max. constraints
        """
        # Decision variables
        self._x = [[Int('x(%d,%d)'%(i,j)) for j in range(self.t)] for i in range(self.n)]
        self._W = [Int('w(%d)'%(j)) for j in range(self.t)]
        self._TW = Int('TW')
        
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
            self._s.add(Or(self._W[j]==0, And(sum([r[j] for r in self._x])>=self.k[j], self._W[j]==self.w[j])))

    def _binary_search(self, TW_low, TW_high):
        """
        """        
        self._s.push()
        print('TW range = [%d,%d]'%(TW_low,TW_high))  
#        raw_input("Press Enter to continue...")
        
        # BASE CASE TW_high - TW_low == 1
        if TW_high-TW_low == 1:
            self._s.add(sum(self._W)==TW_high, self._TW==sum(self._W))
            sat_res = self._s.check()
            self._s.pop()
            if sat_res == sat:
                return (sat_res, TW_high)
            else:
                # Don't really have to do this last check but just to be safe
                self._s.add(sum(self._W)==TW_low, self._TW==sum(self._W))
                return (self._s.check(), TW_low)
        
        # Since we're maximizing, first check the higher half of the range        
        TW_mid = int(math.ceil((TW_low+TW_high)/2))
        self._s.add(sum(self._W)>=TW_mid, sum(self._W)<=TW_high, self._TW==sum(self._W))
        sat_res = self._s.check()
        if sat_res == sat:
            # Next line is an optimization, not 100% certain it will work
#            TW_low = self._s.model()[self._TW].as_long()
            TW_low = TW_mid
        else:
            # if it's not in the higher half then it must be in the lower half
            TW_high = int(math.floor((TW_low+TW_high)/2))
        self._s.pop()
        return self._binary_search(TW_low, TW_high)        
        
        
        