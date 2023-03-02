
import os
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import matplotlib
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
    
    __slots__ = ('NACAnr', 'name', 'n_pts', 'includeTE', 'TE', 'x')
    
    def __init__(self, NACAnr, **kwargs):
        """
        -----------------------------------------------------------------------
        |  Class for creating a NACA airfoil                                  |
        -----------------------------------------------------------------------
        |  INPUT:                                                             |
        |      NACAno (str) : 'NACA profile to be used, fx '2410'             |
        |                                                                     |
        |  OPTIONAL:                                                          |
        |      n_pts (int) : Number of points to be plotted, fx 100           |
        |      includeTE (bool) : True or False for including round           |
        |                         trailing edge                               |
        |      TE (float):   Trailing Edge placement as relative to chord     |
        |                    length, i.e. a nummber between 0 and 1           |
        |_____________________________________________________________________|      
        
        """
        self.NACAnr = NACAnr
        self.name = 'NACA'+ self.NACAnr
        self.n_pts = kwargs.get("n_pts", 100)
        self.includeTE = kwargs.get("includeTE", False) 
        self.TE = kwargs.get("TE", 0.9)         
 
        self.T = float(self.NACAnr[-2:])/100                                   # Max thickness
 
        self.x = np.linspace(0, 1, self.n_pts)
        
        if self.NACAnr.isnumeric():
            
            if len(self.NACAnr) == 4:
                self.four_digit()
                
            elif len(self.NACAnr) == 5:
                self.five_digit()
                
            else:
                raise Exception("Sorry, input NACA number must be a 4 or 5 digit ")
                
            self.calculate_thickness_distribution()
            
        else:
            raise Exception("Sorry, a NACA number only contains digits")
       
            
    def __str__(self):
        return f'A {self.name} airfoil from {self.n_pts} points'

    def __repr__(self):
        return f'NACA(\'{self.NACAnr}\', n_pts={self.n_pts}, includeTE={self.includeTE}, TE={self.TE})'
        
    
    def four_digit(self):
        """
        -----------------------------------------------------------------------
        | Method for creating the four digit NACA Airfoil                     |
        -----------------------------------------------------------------------
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
        M = float(self.NACAnr[0])/100                                          # Maximum camber percentage
        P = float(self.NACAnr[1])/10                                           # Toppoint as fraction of chord
 
        
  
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
        -----------------------------------------------------------------------
        |
        | values for P, M and K taken from : 
            https://web.stanford.edu/~cantwell/AA200_Course_Material/The%20NACA%20airfoil%20series.pdf
        -----------------------------------------------------------------------
        """
        print("Creating five digit NACA Airfoil: "+self.NACAnr)  
  
        if not int(self.NACAnr[2]) in (0,1):
            raise ValueError('Third digit in a 5-digit NACA Airfoil should be 1 or 0')
            
        P = 5 * float(self.NACAnr[1]) / 100  # Top point as fraction of chord

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


    def six_series(self):
        a = 0.3
        b = 1.0           
        cl = 1;
        
        g = -1/(b-a) * ( a**2 * (0.5* np.log(a) -0.25) - b**2 * (0.5 * np.log(b) - 0.25) )   
         
        h = 0
        if 0 <= a < 1:
            h+= 1/(b-a) * (0.5*(1-a)**2 * np.log(1-a))                 
        if 0 <= b < 1:         
            h-= (0.5*(1-b)**2)*np.log(1-b) + 0.25*(1-b)**2 
        if 0 <= a < 1:    
            h-= 0.25*(1-a)**2
        h += g
        
        y  = cl/(2*np.pi*(a+b))*(1/(b-a)*(0.5*(a-x)**2* np.log(abs(a-x)) - 0.5*(b-x)**2*np.log(abs(b-x)) + 0.25*(b-x)**2 - 0.25*(a-x)**2) - x*np.log(x) + g - h*x) 
    
        pts = np.concatenate((x.T[:, None], y.T[:, None]), axis=1)


    def calculate_thickness_distribution(self):
        """
        -----------------------------------------------------------------------
        | Method for calculating the surface points of a NACA Airfoil         |
        |                                                                     |
        -----------------------------------------------------------------------
        """
        theta = np.arctan(self.dyc_dx)
        
        a = np.array([0.2969, -0.1260, -0.3516, 0.2843, -0.1036])
   
        self.yt = 5*self.T*(a[0]*np.sqrt(self.x) + a[1]*self.x + a[2]*(self.x**2) + a[3]*(self.x**3) + a[4]*(self.x**4))
 
        if self.includeTE:
            te_pts = int(np.size(self.yt) * self.TE)
            self.yt =  np.delete(self.yt, np.arange(te_pts, self.n_pts))
            theta = np.delete(theta, np.arange(te_pts, self.n_pts))
            yc = np.delete(self.yc, np.arange(te_pts, self.n_pts))
            self.x = np.delete(self.x, np.arange(te_pts, self.n_pts))
            x_te = np.linspace(np.pi/2 - -theta[-1], 
                               -np.pi / 2 + theta[-1], 
                               2*(self.n_pts - len(self.x))) # Angles
            TEx = self.yt[-1] * np.cos(x_te) + self.x[-1]                      # Trailing edge x-coordinates, parametric circle equation    
            TEy = self.yt[-1] * np.sin(x_te) + yc[-1]                          # Trailing edge y-coordinates, Parametric circle equation    
 
        xu = self.x  - self.yt*np.sin(theta)                                   # Upper surface points
        yu = self.yc + self.yt*np.cos(theta)                                   # Upper surface points
        xl = self.x  + self.yt*np.sin(theta)                                   # Lower surface points
        yl = self.yc - self.yt*np.cos(theta)                                   # Lower surface points      
 
        if self.includeTE:
            Pts_x = np.concatenate((xu, TEx, np.flip(xl)))
            Pts_y = np.concatenate((yu, TEy, np.flip(yl)))   
        else:
            Pts_x = np.append(xu, np.flip(xl))
            Pts_y = np.append(yu, np.flip(yl)) 
 
        self.pts = np.concatenate((Pts_x.T[:, None], Pts_y.T[:, None]), axis=1)
        

    
    def plot(self):
        """
        -----------------------------------------------------------------------
        | Method for plotting the foil created by this class                  |
        -----------------------------------------------------------------------
        """
        fig = plt.figure(figsize=(7, 5))
        ax = fig.add_subplot(111)
        ax.plot(self.x, self.yt, color='green', linestyle='dashed', linewidth=0.5)
      #  ax.plot(xu, yu, color='blue', linestyle='solid', linewidth=1)
       # ax.plot(xl, yl, color='blue', linestyle='solid', linewidth=1)
        ax.plot(self.pts[:,0], self.pts[:,1], color='blue', linestyle='solid', linewidth=1)
        ax.axis('equal')        
        
        
    def save(self, output_folder = r'./export_folder/'):
        """
        -----------------------------------------------------------------------
        | Method for saving the foil created by this class                    |
        -----------------------------------------------------------------------
        |  output_folder (str) : Full path to the output folder of the foil   |
        |                        file. Default to './export_folder/'          |
        |_____________________________________________________________________|
        """
        
        output_path = os.path.join(output_folder, self.NACAnr+'.txt')
        np.savetxt( output_path, self.pts, delimiter=' ', fmt='%1.3f')







class NACAs:
    
    def __init__(self, **kwargs):
        self.nacanrs = []
        self.nacafoils = []
      
        
    @staticmethod     
    def makeall_NACA4nrs():
        """
        -----------------------------------------------------------------------
        | Method for making all the realistic NACA 4 numbers                  |
        -----------------------------------------------------------------------
        """
        naca4nrs = []
        for m in range(10):
            for p in range(1,10):
                for t in range(1,40):
                    if t < 10:
                        t = "0"+str(t)
                    else:
                        t = str(t)
                    nacanumber = str(m)+str(p)+t
               #     print(nacanumber)
                    naca4nrs.append(nacanumber)
        return naca4nrs
                    
    
    @staticmethod
    def makeall_NACA5nrs():
        """
        -----------------------------------------------------------------------
        | Method for making all the realistic NACA 5 numbers                  |
        -----------------------------------------------------------------------
        """
        naca5nrs = []
        for l in range(1,7):
            for p in range(3,5):
                for q in range(2):
                    for t in range(1,40):
                        if t < 10:
                            t = "0"+str(t)
                        else:
                            t = str(t)
                        nacanumber = str(l)+str(p)+str(q)+t
                      #  print(nacanumber)
                        naca5nrs.append(nacanumber)
        return naca5nrs
    
    
    @staticmethod    
    def generate_NACA_foils(nacanrs : list, n_pts=100):
        """
        -----------------------------------------------------------------------
        | Method for generating the objects of all the NACA 4- and 5- digit   |
        | foils supplied in the input list of strings                         |
        -----------------------------------------------------------------------
        """
        nacafoils = []
        for f in nacanrs:
            naca_airfoil = NACA(f, includeTE=False, n_pts=100)
            nacafoils.append(naca_airfoil)   
        return nacafoils
    
    @staticmethod
    def makeall_NACA5():
        naca5nrs = NACAs.makeall_NACA5nrs()
        naca5s = NACAs.generate_NACA_foils(naca5nrs)
        return naca5s


class PlotFoil: 
    def all_from_list(foils):
        fig = plt.figure(figsize=(7, 5))
        ax = fig.add_subplot(111)

        n = len(foils)
        color = matplotlib.cm.rainbow(np.linspace(0, 1, n))

        i = 0
        for _, c in zip(range(n), color):
           #plt.plot(x, y, c=c)
           ax.plot(foils[i].pts[:,0], foils[i].pts[:,1], color=c, linestyle='solid', linewidth=1)
           i +=1
            
        ax.axis('equal')        
          
     


# NACA 6-series:
# "When the mean-line designation is not given, it is understood that 
# the uniform-load mean line (a= 1.0) has been used." 


#65,3-218, a=O.5, 


x = np.linspace(0, 1, 100)

 
a = 0.3
b = 1.0  # caution for NON-unity entries change the equation for h
 
cl = 1;

g = -1/(b-a) * ( a**2 * (0.5* np.log(a) -0.25) - b**2 * (0.5 * np.log(b) - 0.25) )   


h = 0
if 0 <= a < 1:
    h+= 1/(b-a) * (0.5*(1-a)**2 * np.log(1-a))                 
if 0 <= b < 1:         
    h-= (0.5*(1-b)**2)*np.log(1-b) + 0.25*(1-b)**2 
if 0 <= a < 1:    
    h-= 0.25*(1-a)**2
h += g

y  = cl/(2*np.pi*(a+b))*(1/(b-a)*(0.5*(a-x)**2* np.log(abs(a-x)) - 0.5*(b-x)**2*np.log(abs(b-x)) + 0.25*(b-x)**2 - 0.25*(a-x)**2) - x*np.log(x) + g - h*x) 

y = np.concatenate([y, -1*np.flip(y)])
x = np.concatenate([x, np.flip(x)])

pts = np.concatenate((x.T[:, None], y.T[:, None]), axis=1)
fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(111)
ax.plot(pts[:,0], pts[:,1], color='blue', linestyle='solid', linewidth=1)
ax.axis('equal')        
plt.show()
# =============================================================================
# 
# =============================================================================
# =============================================================================
# 
# import time
# 
# t0 = time.time()
# =============================================================================





    
#airfoil.plot()
#yc = airfoil.yc  
# =============================================================================
# a = np.array([0.2969, -0.1260, -0.3516, 0.2843, -0.1036])
# x = np.linspace(0, 1, 100)
#      
# x1, x2 = np.split(x, [int(P*len(self.x))])
#     
# yt1 = a[0]*np.sqrt(x)+a[1] +a[2]*x**2 + a[3]*x**3
# yt2 = d[0]+d[1]*(1-x)+d[2]*(1-x)**2 + d[3]*(1-x)**3
# =============================================================================
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






# =============================================================================
#     def modified(self):
#         """
#         -----------------------------------------------------------------------
#         Explanation:
#         fx NACA 0012-64
#         After dash:
#             - First digit: Roundedness of the nose. 
#                 A value of 6 is the same as the original
#                 A value of 0 indicates a sharp leading edge. 
#                 A value larger than 6 produces a more rounded nose
#             - Second digit: Location of maximum thickness in tenths of chord.
#                 default is 30% back from the leading edge. 
#                 If digit is 4 then it is 40%  
#         -----------------------------------------------------------------------        
#         """
# =============================================================================







