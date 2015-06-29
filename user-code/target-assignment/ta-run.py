# -*- coding: utf-8 -*-

from TASolver import *

n = 4
t = 3
k = [2,3,2]
cst = [(0,2),(1,0),(2,2),(3,0)]
w = [2,5,2]
tas = TASolver()
tas.set_ta_vars(n,t,k,cst,w)
tas.solve()

#tas.show_solution()