import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

# =============================================================================
# class DimensionAirfoil():
#         """
#         -----------------------------------------------------------------------
#         |      c (float)     : Chord length                                   |
#         |      origin (tuple)  : Specifiy airfoil displacement in space,      |
#         |                        i.e., (0,0,0)                                |
#         """
# =============================================================================


class NACA:
    
    def __init__(self, NACAnr, **kwargs):
        """
        -----------------------------------------------------------------------
        |  Class for creating a NACA airfoil                                  |
        -----------------------------------------------------------------------
        |  INPUT:                                                             |
        |      NACAno (str) : '2410'     # NACA profile to be used            |
        |                                                                     |
        |  OPTIONAL:                                                          |
        |      gridPts (int) : Number of points to be plotted, fx 100         |
        |      includeTE (bool) : True or False for including round           |
        |                         trailing edge                               |
        |      TE (float):   Trailing Edge placement as relative to chord     |
        |                    length, i.e. a nummber between 0 and 1           |
        |_____________________________________________________________________|      
        
        """
        self.NACAnr = NACAnr
        self.gridPts = kwargs.get("gridPts", 100)
        self.includeTE = kwargs.get("includeTE", False) 
        self.TE = kwargs.get("TE", 0.9)         
        
        
        self.x = np.linspace(0, 1, self.gridPts)
        
        if self.NACAnr.isnumeric():
            
            if len(self.NACAnr) == 4:
                self.four_digit()
                
            elif len(self.NACAnr) == 5:
                self.five_digit()
                
            else:
                raise Exception("Sorry, input NACA number must be a 4 or 5 digit ")
                
            self.calculate_surface_points()
            
        else:
            raise Exception("Sorry, a NACA number only contains digits")
        
        
    def four_digit(self):
        """
        -----------------------------------------------------------------------
        | Method for creating the four digit NACA Airfoil                     |
        | The first digit is the maximum camber.                              |
        | The second digit is the relative position of the maximum camber.    |
        | The last two digits are the maximum thickness.                      |
        | Fx:                                                                 |
        |        NACA 2514 airfoil                                            |
        |        Max camber 2% at 0.5 chord                                   |
        |        Max thickness 14%                                            |
        |                                                                     |
        -----------------------------------------------------------------------
        """
        
        # Extract values values from the NACA string
        M = float(self.NACAnr[0])/100                                            # Maximum camber percentage
        P = float(self.NACAnr[1])/10                                             # Toppoint as fraction of chord
        self.T = float(self.NACAnr[2:4])/100                                    # Max thickness
        
  
        x1, x2 = np.split(self.x, [int(P*len(self.x))])
    
        yc1 = (M/P**2)*((2*P*x1)-x1**2)      # Camber line
        yc2 = (M/((1-P)**2))*(1-(2*P) + (2*P*x2)-(x2**2))
        dyc_dx1 = ((2*M)/(P**2))*(P-x1)      # Derivative of the camber line
        dyc_dx2 = ((2*M)/((1-P)**2))*(P-x2)
    
        self.yc = np.concatenate((yc1, yc2))
        self.dyc_dx = np.concatenate((dyc_dx1, dyc_dx2))
             
        
    def five_digit(self):
        """
        -----------------------------------------------------------------------
        | Method for creating the five digit NACA Airfoil                     |
        |
        -----------------------------------------------------------------------
        """
        print("Creating five digit NACA Airfoil")  
  
        if int(self.NACAnr[2]) in (0,1):
            print("Acceptable digit")
        else:
            raise ValueError('Third digit in a 5-digit NACA Airfoil should be 1 or 0')
            
        P = 5 * float(self.NACAnr[1]) / 100  # Top point as fraction of chord
        self.T = float(self.NACAnr[3:5]) / 100  # Max thickness

        if int(self.NACAnr[2])==0:
            p = np.array([0.05, 0.1, 0.15, 0.2, 0.25])
            M = np.array([0.0580, 0.1260, 0.2025, 0.2900, 0.3910])
            K = np.array([361.4, 51.64, 15.957, 6.643, 3.230])
        elif int(self.NACAnr[2]) == 1:
            p = np.array([0.1, 0.15, 0.2, 0.25])
            M = np.array([ 0.13, 0.217, 0.318, 0.441])
            K = np.array([ 51.99, 15.793, 6.520, 3.191])

        m = CubicSpline(p, M)(P)
        k1 = CubicSpline(M, K)(m)
        K1_K2 = (3 * (m - P) ** 2 - m ** 3) / ((1 - m) ** 3)

        if int(self.NACAnr[2]) == 0:
           self.yc = ((k1/6)*(self.x**3-3*m*self.x**2+m**2*(3-m)*self.x))*(self.x<P) + (((k1*m**3)/6)*(1-self.x))*(self.x>=P)
        elif int(self.NACAnr[2]) == 1:
            self.yc = ((k1/6)*((self.x-m)**3-K1_K2*(1-m)**3*self.x-m**3*self.x+m**3))*(self.x<P)+((k1/6)*(K1_K2*(self.x-m)**3-K1_K2*(1-m)**3*self.x-m**3*self.x+m**3))*(self.x>=P)
        else:
            raise ValueError
            
        self.dyc_dx = ((k1/6)*(3*self.x**2-6*m*self.x+m**2*(3-m)))*(self.x<P)+(-1*((k1*m**3)/6))*(self.x >= P)


    def calculate_surface_points(self):
        """
        -----------------------------------------------------------------------
        | Method for calculating the surface points of a NACA Airfoil         |
        |                                                                     |
        -----------------------------------------------------------------------
        """
        theta = np.arctan(self.dyc_dx)
        
        a = np.array([0.2969, -0.1260, -0.3516, 0.2843, -0.1036])
   
        self.yt_ini = 5*self.T*(a[0]*np.sqrt(self.x) + a[1]*self.x + a[2]*(self.x**2) + a[3]*(self.x**3) + a[4]*(self.x**4))
 
        if self.includeTE:
            te_pts = int(np.size(self.yt_ini) * self.TE)
            self.yt =  np.delete(self.yt_ini, np.arange(te_pts, self.gridPts))
            theta = np.delete(theta, np.arange(te_pts, self.gridPts))
            yc = np.delete(self.yc, np.arange(te_pts, self.gridPts))
            x = np.delete(self.x, np.arange(te_pts, self.gridPts))
            x_te = np.linspace(np.pi/2 - -theta[-1], 
                               -np.pi / 2 + theta[-1], 
                               2*(self.gridPts - len(x))) # Angles
            TEx = self.yt[-1] * np.cos(x_te) + x[-1]                           # Trailing edge x-coordinates, parametric circle equation    
            TEy = self.yt[-1] * np.sin(x_te) + yc[-1]                          # Trailing edge y-coordinates, Parametric circle equation    
 
        xu = x  - self.yt*np.sin(theta)                                        # Upper surface points
        yu = yc + self.yt*np.cos(theta)                                        # Upper surface points
        xl = x  + self.yt*np.sin(theta)                                        # Lower surface points
        yl = yc - self.yt*np.cos(theta)                                        # Lower surface points      
 
        if self.includeTE:
            Pts_x = np.concatenate((xu, TEx, np.flip(xl)))
            Pts_y = np.concatenate((yu, TEy, np.flip(yl)))   
        else:
            Pts_x = np.append(xu, np.flip(xl))
            Pts_y = np.append(yu, np.flip(yl)) 
 
        self.pts = np.concatenate((Pts_x.T[:, None], Pts_y.T[:, None]), axis=1)
        

    
    def plot(self):
        fig = plt.figure(figsize=(7, 5))
        ax = fig.add_subplot(111)
        ax.plot(self.x, self.yt_ini, color='green', linestyle='dashed', linewidth=0.5)
      #  ax.plot(xu, yu, color='blue', linestyle='solid', linewidth=1)
       # ax.plot(xl, yl, color='blue', linestyle='solid', linewidth=1)
        ax.plot(self.pts[:,0], self.pts[:,1], color='blue', linestyle='solid', linewidth=1)
        ax.axis('equal')        
        








        


# =============================================================================
#         
# =============================================================================
 
 





# =============================================================================
# 
# =============================================================================
# =============================================================================
# 
# import time
# 
# t0 = time.time()
# =============================================================================


airfoil = NACA('24012', includeTE=True, gridPts=10000)
airfoil.plot()
    
# =============================================================================
# t1 = time.time()
# total = t1-t0
# print("Method 1: "+str(total))
# 
# =============================================================================
 

   


#plot_airfoil(airfoil_pts1)

# =============================================================================
# 
# =============================================================================












