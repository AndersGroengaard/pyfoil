

# =============================================================================
#  Single airfoils
# =============================================================================

from foils import NACA

# NACA 4-Digit airfoil:
airfoil = NACA("2310")

# If you want to retrieve the pts:
airfoil_pts = airfoil.pts   

airfoil.plot()
#airfoil.save()


# NACA 5-Digit airfoil:
airfoil2 = NACA("23116")
airfoil2.plot()
#airfoil2.save()



# =============================================================================
#  Mutiple airfoils
# =============================================================================

# Generate mupltiple airfoils by name:
    
    
from foils import NACAs 
 
my_foils = ['1512', '3512', '5512', '7512', '9512']
foils = NACAs(my_foils)
foils.plot()


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
