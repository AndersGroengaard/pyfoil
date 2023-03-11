"""
===============================================================================
 THE PYFOIL PROJECT 2023
===============================================================================
 
    Script containing classes and methods for creating/instantiating 
    airfoil objects.                                                                     
     
    written in Python 3.9 by Anders C. Grøngaard                   
                                                     
===============================================================================
"""    


import os
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import matplotlib
import itertools





def plot_glowing_line(ax, x, y, color, linestyle='solid', linewidth=1, label=""):
    """
    ---------------------------------------------------------------------------
    ---------------------------------------------------------------------------     
    """
    ax.plot(x, y, color=color, linestyle=linestyle, 
            linewidth=linewidth, zorder=2, label=label)
    for w in range(10):
        ax.plot(x, y, lw=w, color=color, 
                zorder=1, alpha=0.05)
  


 

class Foil:
    """
    ---------------------------------------------------------------------------
    | Parent class for all types of foils                                     |
    ---------------------------------------------------------------------------
    """
    
    descr = "Foil Object"
    newid = itertools.count() 
    
    def __init__(self, name):
        self.name = name
        self.id = next(self.newid)
        self.c = 1
        self.x = None
        self.yt = None
        self.base_pts = None
        self.pts = None
   
        
    def set_chord(self, c):
        """
        -----------------------------------------------------------------------
        | Method for scaling the foil chord length                            |
        -----------------------------------------------------------------------
        """
        self.c = c
        self.pts = self.base_pts*self.c
    
    def location(self, loc=(0,0,0)):
        self.pts + loc     
        
        
    def plot(self):
        """
        -----------------------------------------------------------------------
        | Method for plotting the foil created by this class                  |
        -----------------------------------------------------------------------
        """
 
        foil_color = '#08F7FE'
 
        fig = plt.figure(figsize=(7, 5), facecolor='#212946')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#212946')
        
        if self.x is not None and self.yc is not None:
            plot_glowing_line(ax, self.x, self.yc, 
                              '#00ff9f',
                            #  '#ea00d9', 
                              linestyle='dashed', label="camber line")

        ax.fill(self.pts[:,0], self.pts[:,1], color=foil_color, alpha=0.25, zorder=1)      
        plot_glowing_line(ax, self.pts[:,0], self.pts[:,1], foil_color, label="Foil Surface")
   
        ax.axis('equal')        
        ax.set_title(self.name, color='#08F7FE')
 
        plt.grid(color='#2A3459', linestyle='solid')
 
        for spine in ax.spines.values():
            spine.set_visible(False)
 
        ax.tick_params(colors='#DFE0E1', direction='out')
        for tick in ax.get_xticklabels():
            tick.set_color('#DFE0E1')
        for tick in ax.get_yticklabels():
            tick.set_color('#DFE0E1')
            
        ax.set_xlabel('X-axis',fontsize = 10, color='#08F7FE')                
        ax.set_ylabel('Y-axis', fontsize = 10, color='#08F7FE')               
        
        
    def save(self, output_folder = r'./export_folder/'):
        """
        -----------------------------------------------------------------------
        | Method for saving the foil created by this class                    |
        -----------------------------------------------------------------------
        |  output_folder (str) : Full path to the output folder of the foil   |
        |                        file. Default to './export_folder/'          |
        |_____________________________________________________________________|
        """
        
        output_path = os.path.join(output_folder, self.name+'.dat')
        np.savetxt(output_path, self.pts, delimiter=' ', fmt='%1.5f')

    def __str__(self) -> str:
        return f'{self.name}'


 
class DataFoil(Foil):
    
    descr = "DataFoil Object"
    
    def __init__(self, name):
        super().__init__(name)
        """
        -----------------------------------------------------------------------
        |  Class for importing airfoil points from a database based on        |
        |  .dat files                                                         |
        -----------------------------------------------------------------------
        |  INPUT:                                                             |
        |      name (str) : Name of the foil to import, fc "risoe_a_21"       |
        |                                                                     |
        |_____________________________________________________________________|
        """
        foil_path = r'./foil_lib/'+self.name+'.dat'
        
        if os.path.exists(foil_path):
            
            self.base_pts = np.genfromtxt(r'./foil_lib/'+self.name+'.dat', 
                                    skip_header=0, dtype=float, 
                                    invalid_raise=False, 
                                    usecols = (0, 1))
            
            if self.base_pts.shape[1] == 2:                                    # If we only have x and y coordinates, we need to add a z vector as well
                Pts_z = np.zeros(np.size(self.base_pts[:,0]))                  # Initializing z-vector
    
                self.base_pts = np.concatenate((self.base_pts, 
                                           Pts_z.T[:, None]), 
                                           axis=1)
            self.pts = self.base_pts
    
            self.n_pts = len(self.pts) 
            
        
        else:
            raise Exception(f'An airfoil by the name of {self.name} was not found in the database' )
        
    def __str__(self) -> str:
        return f'An {self.name} airfoil imported from a database consisting of {self.n_pts} points'             
 
    def __repr__(self):
        return f'NACA(\'{self.NACAnr}\', n_pts={self.n_pts}, includeTE={self.includeTE}, TE={self.TE})'
        

class NACA(Foil):
    
    descr = "NACA Foil Object"
    
    __slots__ = ('NACAnr', 'name', 'n_pts', 'includeTE', 'TE', 'x', 'cos_space')
    
    def __init__(self, name, **kwargs):
        super().__init__(name)
        """
        -----------------------------------------------------------------------
        |  Class for creating a NACA airfoil                                  |
        -----------------------------------------------------------------------
        |  INPUT:                                                             |
        |      name (str) : NACA profile to be used, fx '2410'                |
        |                                                                     |
        |  OPTIONAL:                                                          |
        |      n_pts (int) : Number of points to be plotted, fx 100           |
        |      includeTE (bool) : True or False for including round           |
        |                         trailing edge                               |
        |      TE (float):   Trailing Edge placement as relative to chord     |
        |                    length, i.e. a nummber between 0 and 1           |
        |_____________________________________________________________________|      
        
        """
        self.NACAnr = self.name
        self.name = "NACA"+self.NACAnr
        self.n_pts = kwargs.get("n_pts", 100)
        self.x_n_pts = int(self.n_pts/2)
        self.includeTE = kwargs.get("includeTE", False) 
        self.TE = kwargs.get("TE", 0.9)         
        self.cos_space = kwargs.get("cos_space", True)       
   
        if self.cos_space:
           beta = np.linspace(0, np.pi, self.x_n_pts)
           self.x = 0.5*(1-np.cos(beta))
        else:
            self.x = np.linspace(0, 1, self.x_n_pts)#, dtype=np.float16)
    
        if len(self.NACAnr) == 4:
            self.four_digit()
            self.calculate_thickness_distribution()        
        elif len(self.NACAnr) == 5:
            self.five_digit()
            self.calculate_thickness_distribution()
        elif len(self.NACAnr) == 6 and self.NACAnr[:2] == "16" and self.NACAnr[2] == "-": # Conditions for a 16-series airfoil
            
            self.TT = float(self.NACAnr[4:6])/100
            self.T = 0.5
            self.I = 4
            self.cL = float(self.NACAnr[3])/10                                 # First digit after dash designates the design lift coefficient in fractions of ten
            
            self.sixteen_series()
            self.calculate_thickness_distribution(t_type='modified')
            
        elif len(self.NACAnr) == 7 and self.NACAnr[4] == '-':                  # NACA Four digit modified
        
            self.I = float(self.NACAnr[5])                                          # Designation of the leading edge radius
            self.T = float(self.NACAnr[6])/10                                       # chordwise position of maximum thickness in tenths of chord
            
            self.four_digit()
            self.calculate_thickness_distribution(t_type='modified')
        else:
            raise Exception("Sorry, could not find an appropriate method for NACA number supplied")
            
        self.calculate_ordinates()
            
    def __str__(self):
        self.string = f'A generated {self.name} airfoil from {self.n_pts} points'    
        if self.includeTE:
            self.string += f' including a rounded trailing edge placed at {self.TE} of chord length'         
        return self.string

    def __repr__(self):
        return f'NACA(\'{self.NACAnr}\', n_pts={self.n_pts}, includeTE={self.includeTE}, TE={self.TE})'
        
    
    def four_digit(self):
        """
        -----------------------------------------------------------------------
        | Method for creating the four digit NACA Airfoil                     |
        -----------------------------------------------------------------------
        | A NACA 4-digit airfoil has the format MPTT                          | 
        | The first digit, M,  is the maximum camber.                         |
        | The second digit, P, is the relative position of the maximum camber.|
        | The last two digits, TT, designate the maximum thickness.           |
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
        self.TT = float(self.NACAnr[2:4])/100                                  # Max thickness
        
 
        x1, x2 = np.split(self.x, [np.argmax(self.x>P)])
    
        if M == 0:
            self.yc = np.zeros(len(self.x))
            self.dyc_dx = np.zeros(len(self.x))
        else:
            yc1 = (M/P**2)*((2*P*x1)-x1**2)                                    # Camber line
            yc2 = (M/((1-P)**2))*(1-(2*P) + (2*P*x2)-(x2**2))
            dyc_dx1 = ((2*M)/(P**2))*(P-x1)                                    # Derivative of the camber line
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
        |    https://web.stanford.edu/~cantwell/AA200_Course_Material/The%20NACA%20airfoil%20series.pdf
        -----------------------------------------------------------------------
        """
        print("Creating five digit NACA Airfoil: "+self.NACAnr)  
  
        if not int(self.NACAnr[2]) in (0,1):
            raise ValueError('Third digit in a 5-digit NACA Airfoil should be 1 or 0')
            
        P = 5 * float(self.NACAnr[1]) / 100                                    # Top point as fraction of chord
        self.TT = float(self.NACAnr[2:4])/100                                  # Max thickness
        
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


    def six_series(self, a=1, cli=1):
        """
        -----------------------------------------------------------------------
        |
        |   a (float) : A number between 0 and 1 -> 
        |         "NACA 6-series airfoils produce a uniform chordwise loading
        |          from the leading edge to the point x/c=a and a linearly 
        |          decreasing load from this point to the trailing edge."
        |       
        |          Defaults to 1 : "When the mean-line designation is not
        |                       given, it is understood that the uniform-load
        |                       mean line (a=1.0) has been used. "
        |        
        | source: 
        | https://ntrs.nasa.gov/api/citations/19930090976/downloads/19930090976.pdf
        |        
        |   cli (float) : Design lift coefficient        
        |        
        -----------------------------------------------------------------------
        """
 
        b = 1       
       
        if b == a:  # Catching a potential division by zero error
            g = 0 
        else:
            g = -1/(b-a)*((a**2)*(0.5*np.log(a) -0.25) - b**2*(0.5*np.log(b) - 0.25))   
         
        h = 0
        if 0 <= a < 1:
            h+= 1/(b-a) * (0.5*(1-a)**2 * np.log(1-a))                 
        if 0 <= b < 1:         
            h-= (0.5*(1-b)**2)*np.log(1-b) + 0.25*(1-b)**2 
        if 0 <= a < 1:    
            h-= 0.25*(1-a)**2
        h += g
        
  
        if b == a:                                                             # Catching a potential division by zero error
            self.yc = (cli/(4*np.pi))* ((np.log(1/(1-self.x))) + self.x* np.log((1-self.x)/self.x))
            self.dyc_dx = (cli*( np.log((1-self.x)/self.x)) - np.log(1-self.x) ) /(4*np.pi)
        else:
            self.yc = cli/(2*np.pi*(a+b))  *  (1/(b-a)*(0.5*(a-self.x)**2* np.log(abs(a-self.x)) - 0.5*(b-self.x)**2*np.log(abs(b-self.x)) + 0.25*(b-self.x)**2 - 0.25*(a-self.x)**2) - self.x*np.log(self.x) + g - h*self.x) 
    
      #  pts = np.concatenate((x.T[:, None], y.T[:, None]), axis=1)

    def sixteen_series(self):
        """
        -----------------------------------------------------------------------
        | The NACA 16-series airfoil family                                   |
        |                                                                     |
        |   An example is:  NACA 16-012                                       |
        |   The first two digits "16" indicates that this is a sixteen series |
        |   airfoil.                                                          |
        |   The first digit after dash designates the design lift             |
        |   coefficient in fractions of ten.                                  |
        |   The last two digits indicate the thickness in % of chord          |
        |_____________________________________________________________________|
        """
       # self.NACAnr = "16-012"

        self.six_series(a=1, cli=self.cL)                                      # The six series method is used to calculate the camberline
 
    def calculate_thickness_distribution(self, t_type="normal"):
        """
        -----------------------------------------------------------------------
        | Method for calculating the thickness distribution of a NACA Airfoil |
        |                                                                     |
        |    Explanation for NACA 4-digit modified:                           |
        |    fx NACA 0012-64                                                  |
        |    After dash:                                                      | 
        |      - First digit: Roundedness of the nose.                        |
        |         A value of 6 is the same as the original                    |
        |         A value of 0 indicates a sharp leading edge.                |
        |         A value larger than 6 produces a more rounded nose          |
        |      - Second digit: Location of max thickness in tenths of chord.  |
        |         default is 30% back from the leading edge.                  |
        |         If digit is 4 then it is 40%                                |
        |                                                                     |
        -----------------------------------------------------------------------        
        """
 
    
        if t_type == "modified": #
          
            # Equtions Source: Geometry for Aerodynamicists
     
            
            d1 = (2.24 - 5.42*self.T + 12.3*self.T**2) / (10*(1-0.878*self.T)) # (A-21) Riegels approximation
            d2 = (0.294 - 2*(1-self.T)*d1) / ((1-self.T)**2)                   # (A-22)
            d3 = (-0.196 + (1-self.T)*d1)/((1-self.T)**3)                      # (A-23)
            
            if self.I <= 8:
                Xi_LE = self.I/6
            else:
                Xi_LE = 10.3933                                                # (A-25)
                
            a0 = 0.296904*Xi_LE                                                # (A-24)
            
            rho1 = (1/5)*(((1-self.T)**2)/(0.588-2*d1*(1-self.T)))             # (A-26)
            
            a1 = (0.3/self.T)-(15/8)*(a0/np.sqrt(self.T)) - (self.T/(10*rho1)) # (A-27)
            a2 = -1*(0.3/(self.T**2))+(5/4)*(a0/(self.T**(3/2))) + 1/(5*rho1)  # (A-28)
            a3 = 0.1/(self.T**3)-((0.375*a0)/(self.T**(5/2)))-(1/(10*rho1*self.T))       # (A-29)
         
            x1, x2 = np.split(self.x, [np.argmax(self.x>self.T)])              # Splitting the x array in two where x hits the T value
            yt1 = 5*self.TT*(a0*np.sqrt(x1) + a1*x1 + a2*(x1**2) + a3*(x1**3)) # (A-19)
            yt2 = 5*self.TT*(0.002 + d1*(1-x2) + d2*((1-x2)**2) + d3*((1-x2)**3)) # (A-20)
            self.yt =  np.concatenate((yt1, yt2))
            
        else:                                                                  # Else, we calculate the thickness distribution using the NACA 4-Digit method
            
            a = np.array([0.2969, -0.1260, -0.3516, 0.2843, -0.1036])
            self.yt = 5*self.TT*(a[0]*np.sqrt(self.x) + a[1]*self.x + a[2]*(self.x**2) + a[3]*(self.x**3) + a[4]*(self.x**4))
     

 
        
    def calculate_ordinates(self):
        """
        -----------------------------------------------------------------------
        | Method for calculating the surface points of a NACA Airfoil         |
        | after the camber line and thickness distribution has been           |
        | calculated.                                                         |
        -----------------------------------------------------------------------
        """
        theta = np.arctan(self.dyc_dx)
        
        if self.includeTE:
            
            #te_pts = int(np.size(self.yt) * self.TE)
            te_pts = np.argmax(self.x>self.TE)
            self.yt =  np.delete(self.yt, np.arange(te_pts, self.n_pts))

            theta = np.delete(theta, np.arange(te_pts, self.n_pts))
            self.yc = np.delete(self.yc, np.arange(te_pts, self.n_pts))
            self.x = np.delete(self.x, np.arange(te_pts, self.n_pts))
            x_te = np.linspace(np.pi/2 - -theta[-1], 
                               -np.pi / 2 + theta[-1], 
                               2*(self.n_pts - len(self.x)))                   # Angles
            
            TEx = self.yt[-1] * np.cos(x_te) + self.x[-1]                      # Trailing edge x-coordinates, parametric circle equation    
            TEy = self.yt[-1] * np.sin(x_te) + self.yc[-1]                     # Trailing edge y-coordinates, Parametric circle equation    
 
        xu = self.x  - self.yt*np.sin(theta)                                   # Upper surface points
        yu = self.yc + self.yt*np.cos(theta)                                   # Upper surface points
        xl = self.x  + self.yt*np.sin(theta)                                   # Lower surface points
        yl = self.yc - self.yt*np.cos(theta)                                   # Lower surface points      
 
        if self.includeTE:
            #Pts_x = np.concatenate((xu, TEx, np.flip(xl)))
           # Pts_y = np.concatenate((yu, TEy, np.flip(yl)))   
            Pts_x = np.concatenate((xu, TEx[1:-2], np.flip(xl)))
            Pts_y = np.concatenate((yu, TEy[1:-2], np.flip(yl)))
        else:
        #    Pts_x = np.append(xu, np.flip(xl))
        #    Pts_y = np.append(yu, np.flip(yl)) 
            Pts_x = np.append(np.flip(xl), xu[1:])
            Pts_y = np.append(np.flip(yl), yu[1:])

        Pts_z = np.zeros(np.size(Pts_y))                                       # Initializing z-vector

        self.base_pts = np.concatenate((Pts_x.T[:, None], 
                                   Pts_y.T[:, None], 
                                   Pts_z.T[:, None]), 
                                   axis=1)
        
        self.pts = self.base_pts

#    if include_TE == 0:
#        Pts_x = np.append(np.flip(xl_c), xu_c[1:])
#        Pts_y = np.append(np.flip(yl_c), yu_c[1:])
#    else:
#        Pts_x = np.concatenate((xu_c, TEx_c[1:-2], np.flip(xl_c)))
#        Pts_y = np.concatenate((yu_c, TEy_c[1:-2], np.flip(yl_c)))


 

class Biconvex(Foil):
    
 
    def __init__(self, name, n_pts=100, **kwargs ):
        super().__init__(name)
        self.n_pts = n_pts
 
        tau = 0.05
 

        Ox = 0.5
        #Oy=-0.45

      #  x1 = 0
     #   x2 = 1
     #   y1 = 0 
      #  y2 = 0

        r = (tau/2) + (1/(8*tau)) 
        Oy = -1*(r-tau)
        x = Ox-r
        y = Oy-r
   

        startAngle = np.arcsin(abs(Oy)/r)
        endAngle = np.pi - startAngle

     #   alpha = np.arccos(abs(Oy)/r)
        t = np.linspace(startAngle, endAngle, self.n_pts)
        x = r*np.cos(t) + Ox
        y = r*np.sin(t) + Oy

   
         
        fig = plt.figure(figsize=(7, 5), facecolor='#212946')
        ax = fig.add_subplot(111)
        ax.plot(x,y)
        ax.axis('equal')
#Biconvex("Test")
# =============================================================================
# 
# =============================================================================





class FoilGroup: 
    def __init__(self):
        print("FoilGroup initialized")
        self.foils = []
 
        
    def plot(self):
        fig = plt.figure(figsize=(7, 5), facecolor='#212946')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#212946')
        n = len(self.foils)
        color = matplotlib.cm.cool(np.linspace(0, 1, n))

        colors = []
        i = 0
        for _, glow_color in zip(range(n), color):
            x = self.foils[i].pts[:,0]
            y = self.foils[i].pts[:,1]          
 
            line = ax.plot(x, y, color=glow_color, linestyle='solid', linewidth=1, zorder=6, label=self.foils[i].name)
            colors.append(glow_color)          
        
            for cont in range(6, 1, -1):
                ax.plot(x, y, lw=cont, color=glow_color, zorder=5,
                    alpha=0.05)
            i +=1
            
        ax.axis('equal')        
        
        plt.grid(color='#2A3459', linestyle='solid')
 
        for spine in ax.spines.values():
            spine.set_visible(False)
 
        ax.tick_params(colors='#DFE0E1', direction='out')
        for tick in ax.get_xticklabels():
            tick.set_color('#DFE0E1')
        for tick in ax.get_yticklabels():
            tick.set_color('#DFE0E1')
 
        ax.set_xlabel('X-axis',fontsize = 10, color='#08F7FE') #xlabel
        ax.set_ylabel('Y-axis', fontsize = 10, color='#08F7FE')#ylabel
        ax.set_title("Airfoil Comparison", color='#08F7FE')

        #plt.legend(loc="upper right", frameon=False, labelcolor='linecolor') 

        leg = ax.legend(loc="upper right", frameon=False)
        
        for color,text in zip(colors,leg.get_texts()):
            text.set_color(color)

class DataFoils:
    def __init__(self, **kwargs):
        super().__init__()
        self.foil_lib_path = "./foil_lib/"
        self.libnrs = []
        
    def list_all(self):
        self.libnrs = os.listdir(self.foil_lib_path)
          
    def import_library_foils(self, libnrs : list):
        """
        -----------------------------------------------------------------------
        | Method for import all airfoils from the library                     |
        | foils supplied in the input list of strings                         |
        -----------------------------------------------------------------------
        """   
        for l in libnrs:
            lib_airfoil = DataFoil(l)
            self.foils.append(lib_airfoil)       
        
    def import_all(self):
        self.list_all()
        self.import_library_foils(self.libnrs)
      
        
        
        
        
class NACAs(FoilGroup):
 
    def __init__(self, nrs=[], **kwargs):
        super().__init__()
        
        self.nrs = nrs
        if len(self.nrs) > 0:
            self.generate_NACA_foils(self.nrs)
        
    @staticmethod
    def allnumbers():
        naca5nrs = NACAs.getall_NACA5nrs()
        naca4nrs = NACAs.getall_NACA4nrs()
        nacanrs = naca4nrs + naca5nrs
        return nacanrs
    
    @staticmethod     
    def naca4nrs():
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
                        t = "0"+str(t)                                         # Thickness should always be two digits so fx "9" should be "09"
                    else:
                        t = str(t)
                    nacanumber = str(m)+str(p)+t
                    naca4nrs.append(nacanumber)
        return naca4nrs
                    
    
    @staticmethod
    def naca5nrs():
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
    
                        naca5nrs.append(nacanumber)
        return naca5nrs
    
    
    def generate_NACA_foils(self, nacanrs : list, n_pts=100):
        """
        -----------------------------------------------------------------------
        | Method for generating the objects of all the NACA 4- and 5- digit   |
        | foils supplied in the input list of strings                         |
        -----------------------------------------------------------------------
        """
    
        for f in nacanrs:
            naca_airfoil = NACA(f, includeTE=False, n_pts=100)
            self.foils.append(naca_airfoil)   
        
    def makeall_NACA5(self):
        self.generate_NACA_foils(NACAs.naca5nrs())
         
    def makeall_NACA4(self):
        self.generate_NACA_foils(NACAs.naca4nrs())
         

 











 
 
#65,3-218, a=O.5, 


# =============================================================================
# x = np.linspace(0, 1, 100)
# 
#  
# a = 0.3
# b = 1.0  # caution for NON-unity entries change the equation for h
#  
# cl = 1;
# 
# g = -1/(b-a) * ( a**2 * (0.5* np.log(a) -0.25) - b**2 * (0.5 * np.log(b) - 0.25) )   
# 
# 
# h = 0
# if 0 <= a < 1:
#     h+= 1/(b-a) * (0.5*(1-a)**2 * np.log(1-a))                 
# if 0 <= b < 1:         
#     h-= (0.5*(1-b)**2)*np.log(1-b) + 0.25*(1-b)**2 
# if 0 <= a < 1:    
#     h-= 0.25*(1-a)**2
# h += g
# 
# y  = cl/(2*np.pi*(a+b))*(1/(b-a)*(0.5*(a-x)**2* np.log(abs(a-x)) - 0.5*(b-x)**2*np.log(abs(b-x)) + 0.25*(b-x)**2 - 0.25*(a-x)**2) - x*np.log(x) + g - h*x) 
# 
# y = np.concatenate([y, -1*np.flip(y)])
# x = np.concatenate([x, np.flip(x)])
# 
# pts = np.concatenate((x.T[:, None], y.T[:, None]), axis=1)
# 
# fig = plt.figure(figsize=(7, 5))
# ax = fig.add_subplot(111)
# ax.plot(pts[:,0], pts[:,1], color='blue', linestyle='solid', linewidth=1)
# ax.axis('equal')        
# plt.show()
# 
# 
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
 

   
 







