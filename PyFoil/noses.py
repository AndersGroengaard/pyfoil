 
# =============================================================================
#  Muligt ting at undersøge:
#    - von Karman ogive, von karman waverider
 
 
import numpy as np
import matplotlib.pyplot as plt

class Nose:
    def __init__(self):
        print("Nosey")
        self.x = None
        self.y = None
        
    def plot(self):    
        fig = plt.figure(figsize=(7, 5), facecolor='#212946')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#212946') 
        ax.plot(self.x, self.y, linestyle='solid', color="green", linewidth=1, zorder=6)

  
 
class Haack(Nose):
    def __init__(self, L=1, R=1, C=0.3333, n_pts=100):
        """
        -----------------------------------------------------------------------
        |  Von Karman & L-V Haack                                             |
        |    LD-Haack (Von Kármán)	C=0                                       |
        |    LV-Haack	            C=1/3                                     |
        |    Tangent	            C=2/3                                     |
        |                                                                     |
        |  Equations source: https://en.wikipedia.org/wiki/Nose_cone_design   |
        |  "LD-Haack where C = 0, is commonly called the Von Kármán ogive."   |
        ----------------------------------------------------------------------- 
        """
        super().__init__()
        self.x = np.linspace(0,L,n_pts)    
        theta = np.arccos(1-(2*self.x)/L)
        self.y = (R/np.sqrt(np.pi)) * np.sqrt(theta - (np.sin(2*theta)/2) + ( C*((np.sin(theta))**3) ))  
         
        
class Power(Nose):
    def __init__(self):    
        super().__init__()
        
class Parabolic(Nose):    
   def __init__(self):    
       super().__init__()
       
if __name__ == "__main__":   
    naese = Haack()
    naese.plot()