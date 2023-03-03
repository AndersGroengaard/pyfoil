

# =============================================================================
#  Single airfoils
# =============================================================================

from foils import NACA

# NACA 4-Digit airfoil:
airfoil = NACA("2310")

# If you want to retrieve the pts:
airfoil_pts = airfoil.pts   

#airfoil.plot()
airfoil.save()


# NACA 5-Digit airfoil:
airfoil2 = NACA("23116")
#airfoil2.plot()
airfoil2.save()



# =============================================================================
#  Mutiple airfoils
# =============================================================================

# Generate mupltiple airfoils by name:
    
    
from foils import NACAs, PlotFoil

my_foils = ['0012-22', '0012-76']

foils = NACAs.generate_NACA_foils(my_foils)
PlotFoil.from_list(foils)


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
