
from scipy import interpolate
import numpy as np
from foils import NACA


class GeometryCalculations:
    """
    ===========================================================================
    || Class for containing geometrical calculations                         ||
    ===========================================================================
    """
    @staticmethod
    def find_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
        """
        -----------------------------------------------------------------------
        | Method for taking two lines and calculating the intersection point  | 
        | The lines are defined as following:                                 |
        |     Line 1:                                                         |
        |         starts at point (x1,y1) and ends in (x2,y2)                 | 
        |     line 2:                                                         |
        |         starts at point (x3,y3) and ends in (x4,y4)                 |
        -----------------------------------------------------------------------
        """
        px = ((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
        py = ((x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
        
        return [px, py]
    
    
    @staticmethod
    def get_angle_between_pts(x_1, y_1, x_2, y_2):
        """
        -----------------------------------------------------------------------
        | Method for calculating the angle between two points, in the
        | positive direction of rotation
        -----------------------------------------------------------------------
        |  INPUT:
        |     
        |  OUTPUT:
        |     theta (float) : The angle in radians
        |______________________________________________________________________
        """
        dy = y_1 - y_2
        dx = x_1 - x_2
        if dx > 0:
            theta =np.arctan(dy/dx)
        elif dx < 0 and type ==0:
            theta = np.arctan(dy/dx) - np.pi
        else:
            theta = np.arctan(dy / dx) - np.pi *-1
        return theta 


class MultiElementAirfoil:
    def __init__(self, foil_pts, frac_cs, f_le, le_r):
        self.foil_pts = foil_pts
        self.frac_cs = frac_cs
        self.f_le = f_le
        self.le_r = le_r
        
        self._correct_foil_pts_orientation()
        self._create_foil_division()
        
    def _correct_foil_pts_orientation(self):
        """
        -----------------------------------------------------------------------
        | Method for determining if our foil points are distributed in the    |
        | positive or negative direction of rotation, starting at the         |
        | trailing edge                                                       |
        .......................................................................
        | INPUT:                                                              |
        |    foil_pts (array) : Array of our foil points with x points in     |
        |                       the 0th column and y points in the 1st column |
        |_____________________________________________________________________|
        """
        test_x = np.diff(self.foil_pts[:,0])
        test_y = self.foil_pts[:-1, 1] + self.foil_pts[1:, 1]
        res=sum(np.multiply(test_x, test_y))
        if res > 0:                                                            # If the result is greater than zero, our foil points are in clockwise direction...
            self.foil_pts = np.flipud(self.foil_pts)                           # ... so we flip the columns vertically to make them counter clockwise
        
 
    def _create_foil_division(foil, frac_cs, f_le, le_r):
        """
        -----------------------------------------------------------------------
        | Takes an airfoil consisting of points in a numpy array and divides  |
        | it in two, fx creating a slat and a main body,                      |
        | or a flap and a main body.                                          |
        -----------------------------------------------------------------------
        |  INPUT:                                                             |
        |      foil (array): Airfoil points array: x-coordinates = column 0,  |
        |                    and y-coordinates = column 1                    
        |      frac_cs (float):  chord length of the new body as
        |                        fraction of airfoil chord
        |      f_le (float):  Location of right body leading edge as 
        |                      fraction of airfoil chord
        |      le_r (float):  Radius of leading edge on right body as 
        |                     a fraction of the local thickness
        |______________________________________________________________________
        """
        c=1
        m = 1000                                                               # Number of points in the fitted function
        tck, u = interpolate.splprep([foil[:-1, 0], foil[:-1, 1]], s=0, per=True)  # Splining the airfoil points
        xi, yi = interpolate.splev(np.linspace(0, 1, m), tck)                  # Evaluate a B-spline or its derivatives.
        dx_dt, dy_dt = (interpolate.splev(np.linspace(0, 1, m), tck, der=1))   # Return the first derivative of the spline 
        d2y_dt2 = (interpolate.splev(np.linspace(0, 1, m), tck, der=2))[1]     # Return the second derivative of the spline

        d2y_dt2[xi > (min(xi)+c*0.1)] = 0                                      # Filtering away the trailing edge for now
        # d2y_dt2[xi < c * 0.15] = 0                                           # Filtering away the trailing edge for now
        # LE_idx = d2y_dt2.argmax() - 0                                        # Finding the index of the leading edge
        LE_idx = abs(d2y_dt2).argmax()
        c_s = frac_cs * c                                                      # Creating the slat chord
        idx = np.abs(xi[:LE_idx] - c_s).argmin()                               # Find index for chord end
        cs0_x = xi[LE_idx]; cs0_y = yi[LE_idx]                                 # Leading edge coordinates
        cs1_x = xi[idx]; cs1_y = yi[idx]                                       # Slat end coordinates

        LE_m = f_le * c                                                        # Location of the main body leading edge
        L_s = np.copy(xi)                                                      # Airfoil Lower surface
        L_s[:LE_idx] = 0                                                       # Only lower surface points are non-zero
        LE_m_t = np.abs(L_s - LE_m).argmin()                                   # Index of Leading edge tangent
        t_local = yi[np.abs(xi[:LE_idx] - LE_m).argmin()] - yi[LE_m_t]         # Local thickness at leading edge main body
        LE_m_r = le_r * t_local                                                # Radius of the main body leading edge
        a = np.arctan((dy_dt[LE_m_t]/dx_dt[LE_m_t]))+np.pi*0.5                 # Tangent at the main body leading edge
        LE_o = (LE_m_r*np.cos(a)+xi[LE_m_t], LE_m_r*np.sin(a)+yi[LE_m_t])      # Origo of the leading edge circle
        t = np.linspace(0, 2 * np.pi, 100)                                     # Points for circle
        LE = [LE_o[0] + LE_m_r*np.cos(t), LE_o[1]+LE_m_r*np.sin(t)]            # Leading edge main body, parametric circle
        con_circle = [cs1_x + LE_m_r * np.cos(t), cs1_y + LE_m_r * np.sin(t)]  # Leading edge main body, parametric circle
        JL_a = (dy_dt[idx] / dx_dt[idx])                                       # Slope
        JL_x = np.linspace(-0.1*cs1_x, cs1_x + 0.1, 10)                        # Construction line, x-coordinates
        JL = (-1/JL_a) * (JL_x-cs1_x) + cs1_y                                  # Construction line
        theta = np.arctan(JL_a)-np.pi/2                                        # Angle
        AJ = (cs1_x+LE_m_r*np.cos(theta), cs1_y+LE_m_r*np.sin(theta))
        AK = ((AJ[0] + LE_o[0]) / 2, (AJ[1] + LE_o[1]) / 2)
        a2 = (AJ[1] - LE_o[1]) / (AJ[0] - LE_o[0])
        KL_x = np.linspace(AK[0], AK[0] + 0.2, 10)
        KL = (-1 / a2) * (KL_x - AK[0]) + AK[1]

        AL = GeometryCalculations.find_intersection(JL_x[0], JL[0], JL_x[-1], JL[-1], KL_x[0], KL[0], KL_x[-1], KL[-1])
        fr = np.sqrt((LE_o[0] - AL[0]) ** 2 + (LE_o[1] - AL[1]) ** 2)          # Upper surface front edge radius
        theta1 = np.arctan((LE_o[1]-AL[1])/(LE_o[0]-AL[0]))+np.pi
        theta2 = JL_a + np.pi / 2
        theta3 = a + np.pi
        x_mbf = np.linspace(theta2, theta1, 50)                                # x-coordinates for main body front
        x_mble = np.linspace(theta1, theta3, 20)                               # x-coordinates for main body leading edge

        r_body_front = (np.vstack((AL[0] + (fr + LE_m_r) * np.cos(x_mbf), AL[1] + (fr + LE_m_r) * np.sin(x_mbf)))).T
        r_body_cut = np.concatenate((r_body_front[:-1, :], (np.vstack((LE_o[0]+LE_m_r*np.cos(x_mble), LE_o[1]+LE_m_r*np.sin(x_mble)))).T))
        l_body_cut = np.copy(r_body_cut)
        l_body_front = np.vstack((xi[idx:LE_m_t], yi[idx:LE_m_t])).T

        r_upper_surface = np.vstack((xi[:idx], yi[:idx])).T
        r_lower_surface = np.vstack((xi[LE_m_t:], yi[LE_m_t:])).T
 
       
        l_body = np.concatenate((np.flipud(l_body_cut), l_body_front))
        r_body = np.concatenate((r_upper_surface, r_body_cut[:-1, :], r_lower_surface))

 

        return l_body, r_body 


 

 


if __name__ == "__main__":

    airfoil = NACA("7411")
    #airfoil.plot()
    #airfoil2.save()
    
    foil = airfoil.pts
     
    test = MultiElementAirfoil.create_foil_division(foil, 0.1, 0.25, 0.1)
     
    slat = test[0]
    slat[:,1] = slat[:,1] - 0.05
    slat[:,0] = slat[:,0] - 0.12
    main_foil = test[1]
    
    
     
    import matplotlib.pyplot as plt
    
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111)
    ax.plot(slat[:,0], slat[:,1], color='red', linestyle='solid', linewidth=1)
    ax.plot(main_foil[:,0], main_foil[:,1], color='blue', linestyle='solid', linewidth=1)
    ax.axis('equal')        
    plt.show()

 