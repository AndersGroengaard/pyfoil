# =============================================================================
# 
#   THE GREATEST FONT AND COLOR LIBRARY IN THE WORLD
#   
#   Made in Python 3.9
# 
# =============================================================================
import numpy as np
import matplotlib.font_manager as fm
from matplotlib.colors import ListedColormap,LinearSegmentedColormap


# =============================================================================
# 
#   Getting the AU fonts (These need to be installed on your system)
# 
# =============================================================================
AU     = fm.FontProperties(fname='C:\Windows\Fonts\AUPassata_RG.ttf')
AUb    = fm.FontProperties(fname='C:\Windows\Fonts\AUPassata_Bold.ttf')
AUl    = fm.FontProperties(fname='C:\Windows\Fonts\AUPassata_Light.ttf')
AUp    = fm.FontProperties(fname='C:\Windows\Fonts\AU_Peto.ttf')
AUlogo = fm.FontProperties(fname='C:\Windows\Fonts\AULogoReg.ttf')
# =============================================================================
# 
#  Defining all the AU colors
# 
# =============================================================================

def norm_rgb(rgb_list):
    return 1/255*(np.array(rgb_list))
    
 
AUlightgrey  = norm_rgb([230,230,230])          # The grey in Aarhus Uni. graphics
AUmapgrey    = norm_rgb([184,184,184])          # The grey used in maps in Aarhus Uni. graphics
AUgrey       = norm_rgb([75,75,74])             # The grey in Aarhus Uni. graphics
AUorange     = norm_rgb([238,127,0])            # AU Orange - THe color of Gorms magnificent beard
AUbrown      = norm_rgb([120,66,26])            # AU Brown - The actual colour of Gorms beard
## The AU blues
AUblue       = norm_rgb([0,36,70])              # The blue in Aarhus Uni. graphics
AUblues      = norm_rgb([25,58,88])             # A lighter shade of AUblue
AUbluegrey   = norm_rgb([127,161,197])          # The blue-grey in Aarhus Uni. graphics
AUlightblue  = norm_rgb([55,159,203])           # The lightblue in Aarhus Uni. graphics
AUblue1      = norm_rgb([0,139,191])            # 50 shades of AUblue
AUblue2      = norm_rgb([0,174,239])
AUblue3      = norm_rgb([0,189,242])
AUblue4      = norm_rgb([110,207,246])
AUblue5      = norm_rgb([185,229,251])
## Reds
AUred        = norm_rgb([226,0,26])             # The red in Aarhus Uni. graphics
AUdarkred    = norm_rgb([107,36,36])            # The dark red in Aarhus Uni. graphics
## Yellows and greens
AUdarkyellow = norm_rgb([123,92,0])             # The dark yellow in Aarhus Uni. graphics
AUyellow     = norm_rgb([250,187,0])            # The yellow in Aarhus Uni. graphics
AUgreen      = norm_rgb([139,173,63])           # The green in Aarhus Uni. graphics
AUdarkgreen  = norm_rgb([119,153,43])           # The dark green in Aarhus Uni. graphics
## Purples and pinks
AUdarkpurple = norm_rgb([40,28,65])             # The dark purple in Aarhus Uni. graphics
AUlightpurple= norm_rgb([101,90,159])           # The light purple in Aarhus Uni. graphics
AUmagenta    = norm_rgb([95,0,48])              # The magenta in Aarhus Uni. graphics
AUpink       = norm_rgb([226,0,122])            # The pink in Aarhus Uni. graphics
AUpink1      = norm_rgb([226,73,155])           # 50 shades of AUpink
AUpink2      = norm_rgb([226,93,164])           # 
AUpink3      = norm_rgb([226,111,172])          # 
AUpink4      = norm_rgb([226,128,180])          #
## Weak, non AU colours...
scarfred     = norm_rgb([180,0,0])              # Color of the sikh turban
taskegul     = norm_rgb([255,220,0])            # Yellow color of Julie's bag
mybrown      = norm_rgb([163,101,67])           # A brown color
grey         = norm_rgb([210,210,210])          # A good base grey
Snurple      = norm_rgb([190,78,150])           # The colour of Snoeffler


# =============================================================================
#  Converting to hex
# =============================================================================

def RGBtoHex(vals, rgbtype=1):
    """
    ---------------------------------------------------------------------------
    | Converts RGB values in a variety of formats to Hex values.              |
    ---------------------------------------------------------------------------
    | @param  vals (tuple) :   An RGB/RGBA tuple 
    | @param  rgbtype (int) :  Valid valus are:
    |                          1 - Inputs are in the range 0 to 1
    |                          256 - Inputs are in the range 0 to 255
    |
    | @return (str) :        A hex string in the form '#RRGGBB' or '#RRGGBBAA'
    |__________________________________________________________________________
    """

    if len(vals)!=3 and len(vals)!=4:
      raise Exception("RGB or RGBA inputs to RGBtoHex must have three or four elements!")
    if rgbtype!=1 and rgbtype!=256:
      raise Exception("rgbtype must be 1 or 256!")
    
    if rgbtype==1:                                                             # Convert from 0-1 RGB/RGBA to 0-255 RGB/RGBA
      vals = [255*x for x in vals]
    
    return '#' + ''.join(['{:02X}'.format(int(round(x))) for x in vals])       # Ensure values are rounded integers, convert to hex, and concatenate

 
# =============================================================================
#
#  Creating Custom Color Maps
#
# =============================================================================

AURedGreen =  LinearSegmentedColormap.from_list('AURedGreen', [AUdarkred, AUgreen] , 255)
AUBluePink =  LinearSegmentedColormap.from_list('AUBluePink', [AUblue, AUpink] , 255)
AUBlueBlue =  LinearSegmentedColormap.from_list('AUBlueBlue', [AUblues, AUblue4] , 255)
AUBlueBlue_r =  LinearSegmentedColormap.from_list('AUBlueBluer', [AUblue4, AUblues] , 255)
AUPinkPink =  LinearSegmentedColormap.from_list('AUPinkPink', [AUpink, AUpink4] , 255)
AUYellowPurple =  LinearSegmentedColormap.from_list('AUYellowPurple', [AUyellow, AUlightpurple] , 255)
AUBlueOrange =  LinearSegmentedColormap.from_list('AUBlueOrange', [AUblue1, AUorange] , 255)
AURedOrange =  LinearSegmentedColormap.from_list('AURedOrange', [AUdarkred,AUorange] , 255)
AUGreenGreen =  LinearSegmentedColormap.from_list('AUGreenGreen', [AUdarkgreen,AUgreen] , 255)
