 

from scipy import interpolate
import numpy as np

from foils import NACA

airfoil = NACA("7411")
#airfoil.plot()
#airfoil2.save()

foil = airfoil.pts

f







spline_pts = 1000                                                              # Number of points in the fitted function
tck, u = interpolate.splprep([foil[:-1, 0], foil[:-1, 1]], s=0, per=True)      # Splining the airfoil points
xi, yi = interpolate.splev(np.linspace(0, 1, spline_pts), tck)                 # Evaluate a B-spline or its derivatives.
dx_dt, dy_dt = (interpolate.splev(np.linspace(0, 1, spline_pts), tck, der=1))  # Return the first derivative of the spline 
d2y_dt2 = (interpolate.splev(np.linspace(0, 1, spline_pts), tck, der=2))[1]    # Return the second derivative of the spline
d2y_dt2[xi > (min(xi)+1*0.1)] = 0                                              # Filtering away the trailing edge for now
LE_idx = abs(d2y_dt2).argmax()                                                 # Finding the index of the leading edge

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

# 
# =============================================================================
# =============================================================================
# tcktuple
# (t,c,k) a tuple containing the vector of knots, the B-spline coefficients, and the degree of the spline.
# 
# uarray
# An array of the values of the parameter.
# 
# fpfloat
# The weighted sum of squared residuals of the spline approximation.
# 
# ierint
# An integer flag about splrep success. Success is indicated if ier<=0. If ier in [1,2,3] an error occurred but was not raised. Otherwise an error is raised.
# =============================================================================
