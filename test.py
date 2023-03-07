import numpy as np
from matplotlib.pyplot import *

tau = 0.05

n_pts = 100

Ox = 0.5
#Oy=-0.45

x1 = 0
x2 = 1
y1 = 0 
y2 = 0

r = (tau/2) + (1/(8*tau))#np.sqrt((x1-Ox)*(x1-Ox) + (y1-Oy)*(y1-Oy))
Oy = -1*(r-tau)
x = Ox-r
y = Oy-r
width = 2*r
height = 2*r

startAngle = np.arcsin(abs(Oy)/r)
endAngle = np.pi - startAngle

alpha = np.arccos(abs(Oy)/r)
t = np.linspace(startAngle, endAngle, n_pts)
x = r*np.cos(t) + Ox
y = r*np.sin(t) + Oy

plot(x,y)
axis('equal')

