

# =============================================================================
#  Single airfoils
# =============================================================================

from foils import NACA, DataFoil

# NACA 4-Digit airfoil:
airfoil = NACA("6409")

# If you want to retrieve the pts:
airfoil_pts = airfoil.pts   

airfoil.plot()
#airfoil.save()


# =============================================================================
# # NACA 5-Digit airfoil:
# airfoil2 = NACA("23116")
# airfoil2.plot()
# #airfoil2.save()
# 
# airfoil3 = NACA("7314-33")
# airfoil3.plot()
# =============================================================================



# =============================================================================
# airfoiL5 = DataFoil("s8052")
# airfoiL5.set_chord(5.12)
# #airfoiL5.plot()
# print(airfoiL5)
# =============================================================================
# 
# =============================================================================
#  Mutiple airfoils
# =============================================================================

from foils import NACAs

my_foils = ['9510','9515','9520','9525','9530']
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
