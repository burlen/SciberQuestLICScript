##########################################################################
# sq-lic-driver.py configuration
##########################################################################

# color lookup tables
# if you need one that's not here or you need more control
# fine tune in the pv gui , export, and add the resulting file
# to this list. Unless it's overiden the range from the current
# timestep will be used.
lutFiles                   = ['/home/01237/bloring/apps/all_mpl_cmaps.xml',
                              '/home/01237/bloring/apps/all_idl_cmaps.xml']
# Spectral, BLUE-WHITE, Haze, B-W_LINEAR, Set1, Set2,
# Set3, Rainbow18, BLUE-GREEN-RED-YELLOW, STD_GAMMA-II, Dark2, Hue_Sat_Lightness_1,
# Hue_Sat_Lightness_2, RdPu, YlGnBu, RED-PURPLE, Blue_Waves, RdYlBu,
# Volcano, cool, gray, gist_stern, GnBu, gist_ncar,
# gist_rainbow, STEPS, Mac_Style, bone, Rainbow, RdYlGn,
# Accent, Blue-Red, BLUE-RED, PuBu, STERN_SPECIAL, Plasma,
# Pastels, Rainbow_white, gist_yarg, BuGn, Greens, PRGn,
# gist_heat, Paired, Rainbow_black, GRN-RED-BLU-WHT, Pastel2, Pastel1,
# gist_earth, copper, OrRd, Nature, BuPu, Oranges,
# Purple-Red_Stripes, PiYG, 16_LEVEL, YlGn, GREEN-PINK, Blue_-_Pastel_-_Red,
# GREEN-WHITE_LINEAR, gist_gray, flag, Hue_Sat_Value_2, Hue_Sat_Value_1, BrBG,
# Reds, RdGy, PuRd, RED_TEMPERATURE, Blues, autumn,
# PRISM, Beach, binary, RdBu, hot, YlOrBr,
# Waves, RAINBOW, Eos_A, Hardcandy, Peppermint, Ocean,
# Purples, GRN-WHT_EXPONENTIAL, Greys, YlOrRd, Eos_B, PuOr,
# PuBuGn,

# reader
inputFileName              = '/scratch/01237/bloring/kh-new-all/jaguar-all/jaguar.bov'
arraysToRead               = ['B', 'e-mix1']
iSubset                    = [-1, -1] # subset to read, if < 0 the extent on disk is used
jSubset                    = [-1, -1]
kSubset                    = [-1, -1]

# smoothing
smoothingArraysToFilter    = ['all']# a list of array names, or 'all', or left empty to skip
smoothingWidth             = '3'    # kernel width, must be at least 3

# vortex detection algorithms
vorticityArrayToFilter     = ''     # array to compute on
vorticityArraysToCopy      = []     # a list of array names or 'all'
vorticitySplitComponents   = 0      # results are split into component arrays
vorticityColorByArray      = ''     # if set this array will be rendered
vorticityLutName           = ''     # select a LUT
vorticityLutRange          = []     # force a range on the lut (empty for array bounds)
computeVorticity           = 1      # result is named rot-XX
computeHelicity            = 0      # result is named hel-XX
computeNHelicity           = 0      # result is named norm-hel-XX
computeLambda2             = 0      # result is named lam2-XX
computeDivergence          = 0      # result is named div-XX
computeMagnitudes          = 0      # result is named mag-XX
computeQ                   = 0      # result is named q-XX
computeGradient            = 0      # result is named grad-XX
computeEigenDiagnostic     = 0      # result is named

# lic
LICAlpha                   = 1.0    # controls blending with other rendered objects
LICColorByArray            = 'e-mix1'  # if set this array will be rendered
LICLutName                 = 'Spectral'# select a LUT for the LIC
LICLutRange                = []     # force a range on the lut (empty for array bounds)
LICField                   = 'B'    # vector to LIC on
LICSteps                   = 15     # number of integrator steps
LICStepSize                = 1.0    # integrator step size in pixels
LICIntensity               = 1.00   # controls blending with itself

# slice
sliceAlpha                 = 0.80   # if  0 < sliceAlpha < 1 slice  is rendered
sliceColorByArray          = 'e-mix1' # if set this array is rendered on blended slice
sliceLutName               = 'Spectral' # select a LUT
sliceLutRange              = []     # force a range on the lut (empty for array bounds)

# transformations
translate                  = []     # translation for each coord (empty for none)
scale                      = []     # scale for each coord (empty for none)
rotation                   = [0,0,90] # rotation about each axis (empty for none)
origin                     = []     # origin (empty for none)

# camera
camZoom                    = 1.98   # controls the zoom of the camera, values > 1 zoom in.
camUp                      = []     # override the camera up. (empty for default)
camPos                     = []     # override the camera position. (empty for default)
camFoc                     = []     # override the camera focal point. (empty for default)

# writer
# output prefix, including path, ends in _
outputBaseFileName         = '/scratch/01237/bloring/kh-new-all/lic-b-e-mix-large/lic-b-e-mix_'
outputWidth                = 548    # image width in pixels, or -1 to use defualt
outputHeight               = 1024   # image height in pixels, or -1 to use default
outputMag                  = 1      # integer multiplier on the final rendered image

