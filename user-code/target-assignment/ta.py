# -*- coding: utf-8 -*-
"""
Created on Tue Jun 09 16:19:26 2015

@author: Anshul
"""

from z3 import *

vars = [None] * 2;
vars[0] = Real('x' + str(0))
vars[1] = Real('x' + str(1))

#x = Real('x')
#y = Real('y')
s = Solver()
#s.add(x + y > 5, x > 1, y > 1)
s.add(vars[0] + vars[1] > 5, vars[0] > 1, vars[1] > 1)
print(s.check())
print(s.model())
