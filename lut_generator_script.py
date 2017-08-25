import create3DLUT
import os.path
import datetime

##inputs from front end
lut_size = 65
display_space = 'p3'
aces_type = 'acescct'
lut_type = 'cube'

###
lut_1D_exists = False
lut_name = os.path.join('AMPAS_3Dlut_' + display_space + '_' aces_type + '_%s' %(datetime.datetime.now()))
lut_min = 0
lut_max = 1

lut_3D = create3DLUT.design_3D_lut(lut_size, display_space, aces_type, lut_type)

#### optimization goes here

lut_file = create3DLUT.write_lut(lut_type, lut_3D, lut_1D_exists, lut_name, lut_size, lut_min, lut_max, lut_1D=None)