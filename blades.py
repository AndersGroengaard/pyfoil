# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 20:45:00 2023

@author: ander
"""
import numpy as np

class Blade:
    def __init__(self, L):
        
        self.L = L     # Total Blade length 
        self.R = R     # Radius of wind turbine rotor
        self.nf = 20   # Number of foils
        r
        N = 3 # Number of blades
        cL = 1 # Lift coefficient
        phi = 1 # inflow angle
        cr = (8*np.pi*r)/(N*cL)*(np.sin(phi))/(3*lambda_r)
# =============================================================================
#         b1 = TC - a1*r_tc
#         
#         cr = a1*r+b1
#         thetar = a2*(self.R-r)
# =============================================================================
