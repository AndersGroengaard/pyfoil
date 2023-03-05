# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 11:13:25 2023

@author: ander
"""
# =============================================================================
#  Muligt ting at undersøge:
#    - von Karman ogive, von karman waverider
#    - nose cone design
#    - LH Haack
# =============================================================================
 
import numpy as np
import matplotlib.pyplot as plt

def lvhaack():
    """
    Von Karman & L-V Haack 
    """
   
    nose_length=12   
    cone_diameter=2  #diameter  
    x_res=.01 
    k=0    
    C=0.333333     
    
    x_arr = np.linspace(0,x_res, nose_length)    
    x=x_arr/nose_length;    
    h=np.arccos(1-2*x);   
    r= np.sqrt((h-(1/2)*np.sin(2*h)+(C*((np.sin(h))**3)*h))/np.pi);  
    r=r*(cone_diameter*2);
    
    
 
    fig = plt.figure(figsize=(7, 5), facecolor='#212946')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#212946')
 
    ax.plot(x, r, linestyle='solid', linewidth=1, zorder=6)
 

#lvhaack()