# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 20:45:00 2023

@author: ander
"""

import numpy as np
import matplotlib.pyplot as plt

from foils import NACA, DataFoil

class Blade:
    def __init__(self, R, nf):
         
        self.fn = 20                                                           # Number of foils
        self.r = np.linspace(0, R, self.fn)
# =============================================================================
#         self.L = L     # Total Blade length 
#         self.R = R     # Radius of wind turbine rotor
#         
#         r
#        
#         cL = 1 # Lift coefficient
#         phi = 1 # inflow angle
#         cr = (8*np.pi*r)/(N*cL)*(np.sin(phi))/(3*lambda_r)
# =============================================================================
# =============================================================================
#         b1 = TC - a1*r_tc
#         
#         cr = a1*r+b1
#         thetar = a2*(self.R-r)
# =============================================================================



fn = 20
R = 10
 
r = np.linspace(0, R, fn)

cr = -0.02*r+1

airfoils = []
for i in range(len(r)):
    c = cr[i]
    r_i = r[i]
    
    f = NACA('2412')
    f.set_chord(c)
    
    airfoils.append(f)












