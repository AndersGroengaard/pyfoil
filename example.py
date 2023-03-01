

# =============================================================================
#  Single airfoils
# =============================================================================

from naca import NACA

# NACA 4-Digit airfoil:
airfoil = NACA("2310")
airfoil.plot()
airfoil.save()


# NACA 5-Digit airfoil:
airfoil = NACA("23116")
airfoil.plot()
airfoil.save()