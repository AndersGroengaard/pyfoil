

# =============================================================================
#  Single airfoils
# =============================================================================

from foils import NACA, DataFoil

# NACA 4-Digit airfoil:
airfoil = NACA("6409", includeTE=True, cos_space=True)

# If you want to retrieve the pts:
airfoil_pts = airfoil.pts   

#airfoil.plot()
#airfoil.save()


# NACA 5-Digit airfoil:
airfoil2 = NACA("23116", includeTE=True, cos_space=True)
#airfoil2.plot()
#airfoil2.save()

airfoil3 = NACA("7314-33", includeTE=True, cos_space=True)
airfoil3.plot()

airfoil4 = NACA("7314-33", includeTE=True, cos_space=False)
airfoil4.plot()


airfoiL5 = DataFoil("s8052")
airfoiL5.set_chord(5.12)
#airfoiL5.plot()
print(airfoiL5)
# 
# =============================================================================
#  Mutiple airfoils
# =============================================================================

#import numpy as np
#x = np.linspace(0, 1, 10)
# Generate mupltiple airfoils by name:
#test = x > 0.4
#x1, x2 = np.split(x, [np.argmax(x>0.3)])
#from foils import NACAs 
 
# =============================================================================
# my_foils = ['1512', '3512', '5512', '7512', '9512']
# foils = NACAs(my_foils)
# foils.plot()
# =============================================================================


#foils = NACAs()




#import sys
#print("Airfoil object size is: " + str(sys.getsizeof(airfoil)) + " bytes")
#print("Airfoil objects sizes are: " + str(sys.getsizeof(foils)) + " bytes")
# =============================================================================
# foils = NACAs.makeall_NACA5()
# PlotFoil.all_from_list(foils)
# 
# 
# 
# nacas = NACAs.makeall_NACA4nrs()
# nacas.generate_NACA_foils()
# 
# =============================================================================
