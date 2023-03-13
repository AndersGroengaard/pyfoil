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


class Helix:
    def __init__(self, R_r, H_r, c, n_sections=10, N_b=3):
        
        self.N_b = N_b                                                         # Number of blades
        self.R_r = R_r                                                         # Rotor Radius [m]
        self.H_r = H_r                                                         # Rotor Height [m]
        self.c = c                                                             # Chord length of airfoil [m]
        self.n_sections = n_sections                                           # Number of airfoil sections to use
    
        theta = np.linspace(0, 2*np.pi, self.n_sections)                       # Blade angle
        B_theta = np.linspace(0, 2*np.pi/N_b, self.n_sections)                 # Blade revolution [rad]
        helix_x = (R_r*np.cos(B_theta)).reshape((-1, 1))
        helix_y = (R_r*np.sin(B_theta)).reshape((-1, 1))
        helix_z = (np.linspace(0, H_r, n_sections)).reshape((-1, 1))
        helix = np.hstack([helix_x, helix_y, helix_z])                          
        
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.plot(R_r*np.cos(theta), R_r*np.sin(theta), np.zeros(len(theta)), 
                color='grey', alpha=0.5, linestyle='dashed')
        ax.plot(R_r*np.cos(theta), R_r*np.sin(theta), np.ones(len(theta))*H_r, 
                color='grey', alpha=0.5, linestyle='dashed')
        ax.plot(helix[:, 0], helix[:, 1], helix[:, 2], 
                color="blue", label="Blade Center Line")
        #ax.plot(airfoil[:, 0], airfoil[:, 1], airfoil[:, 2], color=au.black, alpha=0.8)
        ax.set_box_aspect([1, 1, 1])
        ax.legend()
        plt.show()
        
    
if __name__ == "__main__":
   
    
    R_r = 550*1e-3               
    H_r = 1430*1e-3             
    c = 250*1e-3                 
            
    Helix(R_r, H_r, c)
    
    
# =============================================================================
# 
# fn = 20
# R = 10
#  
# r = np.linspace(0, R, fn)
# 
# cr = -0.02*r+1
# 
# airfoils = []
# for i in range(len(r)):
#     c = cr[i]
#     r_i = r[i]
#     
#     f = NACA('2412')
#     f.set_chord(c)
#     
#     airfoils.append(f)
# 
# 
# =============================================================================










