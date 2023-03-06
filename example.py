

# =============================================================================
#  Single airfoils
# =============================================================================

from foils import NACA, DataFoil

# NACA 4-Digit airfoil:
airfoil = NACA("6409")

# If you want to retrieve the pts:
airfoil_pts = airfoil.pts   

#airfoil.plot()
#airfoil.save()


# NACA 5-Digit airfoil:
airfoil2 = NACA("23116")
#airfoil2.plot()
#airfoil2.save()

airfoil3 = NACA("7314-33")
airfoil3.plot()


airfoil4 = NACA("16-009")
airfoil4.plot()

airfoil4 = NACA("16-512")
airfoil4.plot()

airfoil6 = NACA("16-521")
airfoil6.plot()

airfoil76 = NACA("16-530")
airfoil76.plot()

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
