import colour, numpy, OpenEXR, Imath, create3DLUT

"""
	title::
		design_3D_lut

	description::
		This method creates a 3D LUT using CTL transforms and awesomeness. 

	attributes::
		number_lut_nodes = the number of nodes in LUT (17, 33, 65, etc)
		display space = desired display space for the image
		aces_type = desired ACES curve
		lut_type = desired final lut file format; used to determine fastest color channel

	author::
		Emily Faw
		20170824
"""


def design_3D_lut(number_lut_nodes, display_space, aces_type, lut_type):


#################### DISPLAY SPACES ##########################################
	if display_space == 'RGB_monitor':
		inv_odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/rgbMonitor/InvODT.Academy.RGBmonitor_100nits_dim.ctl'
		odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/rgbMonitor/ODT.Academy.RGBmonitor_100nits_dim.ctl'

		# inv_odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/rgbMonitor/InvODT.Academy.RGBmonitor_D60sim_100nits_dim.ctl'
		# odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/rgbMonitor/ODT.Academy.RGBmonitor_D60sim_100nits_dim.ctl'

	if display_space == 'rec2020':

		inv_odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/rec2020/InvODT.Academy.Rec2020_100nits_dim.ctl'
		odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/rec2020/ODT.Academy.Rec2020_100nits_dim.ctl'

	if display_space == 'rec709':

		inv_odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/rec709/InvODT.Academy.Rec709_100nits_dim.ctl'
		odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/rec709/ODT.Academy.Rec709_100nits_dim.ctl'

		# inv_odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/rec709/InvODT.Academy.Rec709_D60sim_100nits_dim.ctl'
		# odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/rec709/ODT.Academy.Rec709_D60sim_100nits_dim.ctl'

	if display_space == 'p3':

		inv_odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/p3/InvODT.Academy.P3D60_48nits.ctl'
		odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/p3/ODT.Academy.P3D60_48nits.ctl'

		# inv_odt = '//Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/p3/InvODT.Academy.P3DCI_48nits.ctl'
		# odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/p3/ODT.Academy.P3DCI_48nits.ctl'

	if display_space == 'hdr_st2084':

		inv_odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/hdr_st2084/InvODT.Academy.P3D60_ST2084_1000nits.ctl'
		odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/hdr_st2084/ODT.Academy.P3D60_ST2084_1000nits.ctl'

	if display_space == 'dcdm':

		inv_odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/dcdm/InvODT.Academy.DCDM.ctl'
		odt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/ODT_transforms/dcdm/ODT.Academy.DCDM.ctl'


################### ACES TYPES ################################################
	if aces_type == 'acescc':

		lin2aces_type = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/aces_transforms/ACEScc/ACEScsc.ACES_to_ACEScc.ctl'
		aces_type2aces = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/aces_transforms/ACEScc/ACEScsc.ACEScc_to_ACES.ctl'

	if aces_type == 'acescct':

		lin2aces_type = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/aces_transforms/ACEScct/ACEScsc.ACES_to_ACEScct.ctl'
		aces_type2aces = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/aces_transforms/ACEScct/ACEScsc.ACEScct_to_ACES.ctl'

	if aces_type == 'acescg':

		lin2aces_type = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/aces_transforms/ACEScg/ACEScsc.ACES_to_ACEScg.ctl'
		aces_type2aces = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/aces_transforms/ACEScg/ACEScsc.ACEScg_to_ACES.ctl'

################### LUT TYPES ################################################

	if lut_type == 'cube':
		fast_channel = 'red'
	if lut_type == 'csp':
		fast_channel = 'red'
	else:
		fast_channel = 'blue'

################# RRT ##############################

	inv_rrt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/RRT_transforms/InvRRT.ctl'
	rrt = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/RRT_transforms/RRT.ctl'


	min_cv = 0 
	max_cv = 1 

	#################### 1D LUT MIN ##########

	min_cv_arr = numpy.array([[min_cv, min_cv, min_cv],[min_cv, min_cv, min_cv],[min_cv, min_cv, min_cv]])
	min_image = create3DLUT.exr2ctl2arr(min_cv_arr, 3, 3, [inv_odt, inv_rrt])

	aces_min = min_image[0,0,0]
	print('aces_min', aces_min)

	################# 1D LUT MAX ################

	max_cv_arr = numpy.array([[max_cv, max_cv, max_cv],[max_cv, max_cv, max_cv],[max_cv, max_cv, max_cv]])
	max_image = create3DLUT.exr2ctl2arr(max_cv_arr, 3, 3, [inv_odt, inv_rrt])

	aces_max = max_image[0,0,0]
	print('aces_max', aces_max)

	#############################

	number_nodes_1D = 4095

	lut1D_nodes = numpy.linspace(aces_min, aces_max, num=number_nodes_1D)

	######################## 3D LUT MIN ###############

	min_3d_pixels = numpy.array([[aces_min, aces_min, aces_min],[aces_min, aces_min, aces_min],[aces_min, aces_min, aces_min]])
	min_3d_image = create3DLUT.exr2ctl2arr(min_3d_pixels, 3, 3, [lin2aces_type])

	min_acescct = min_3d_image[0,0,0]
	print('min aces', min_acescct)

	##################### 3D LUT MAX ######################

	max_3d_pixels = numpy.array([[aces_max, aces_max, aces_max],[aces_max, aces_max, aces_max],[aces_max, aces_max, aces_max]])
	max_3d_image = create3DLUT.exr2ctl2arr(max_3d_pixels, 3, 3, [lin2aces_type])


	max_acescct = max_3d_image[0,0,0]
	print('max aces', max_acescct)

	############### BUILDING 3D LUT ####################### 

	cube_aces = create3DLUT.build_3D_lut(min_acescct, max_acescct, number_lut_nodes, fast_channel)

	################# convert from acesccwhatever to aces  ##########################
	r = cube_aces[:, 0].astype(numpy.float16).tostring()
	g = cube_aces[:, 1].astype(numpy.float16).tostring()
	b = cube_aces[:, 2].astype(numpy.float16).tostring()

	HEADER = OpenEXR.Header(1,number_lut_nodes**3)
	half_chan = Imath.Channel(Imath.PixelType(Imath.PixelType.HALF))
	HEADER['channels'] = dict([(c, half_chan) for c in "RGB"])
	cube_exr = OpenEXR.OutputFile("cube.exr", HEADER)
	cube_exr.writePixels({'R': r, 'G': g, 'B': b})
	cube_exr.close()

	call_ctl_cube = colour.utilities.ctl_render('cube.exr', 'cube_out.exr', [aces_type2aces])

	cube_im = OpenEXR.InputFile('cube_out.exr')
	(r_cube,g_cube,b_cube) = cube_im.channels("RGB")
	dw = cube_im.header()['dataWindow']
	size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

	red_cube = numpy.reshape(numpy.fromstring(r_cube, dtype=numpy.float16), (size[0], size[1]))
	green_cube = numpy.reshape(numpy.fromstring(g_cube, dtype=numpy.float16), (size[0], size[1]))
	blue_cube = numpy.reshape(numpy.fromstring(b_cube, dtype=numpy.float16), (size[0], size[1]))

	cube_image = numpy.stack((red_cube, green_cube, blue_cube), axis=-1) 
	print(cube_image)

	################## now run cube through rrt and odt ############################

	lut_pixels = cube_image.astype(numpy.float16).tostring()
	red = red_cube.astype(numpy.float16).tostring()
	green = green_cube.astype(numpy.float16).tostring()
	blue = blue_cube.astype(numpy.float16).tostring()


	HEADER = OpenEXR.Header(1, number_lut_nodes**3) 
	half_chan = Imath.Channel(Imath.PixelType(Imath.PixelType.HALF))
	HEADER['channels'] = dict([(c, half_chan) for c in "RGB"])
	lut_exr = OpenEXR.OutputFile("lut.exr", HEADER)
	lut_exr.writePixels({'R': red, 'G': green, 'B': blue})
	lut_exr.close()

	call_ctl_lut = colour.utilities.ctl_render('lut.exr', 'lut_out.exr', [rrt, odt])

	lut_im = OpenEXR.InputFile('lut_out.exr')
	(r_lut,g_lut,b_lut) = lut_im.channels("RGB")
	dw = lut_im.header()['dataWindow']
	size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

	red_lut = numpy.reshape(numpy.fromstring(r_lut, dtype=numpy.float16), (size[0], size[1]))
	green_lut = numpy.reshape(numpy.fromstring(g_lut, dtype=numpy.float16), (size[0], size[1]))
	blue_lut = numpy.reshape(numpy.fromstring(b_lut, dtype=numpy.float16), (size[0], size[1]))



	lut = numpy.reshape(numpy.array((red_lut, green_lut, blue_lut)), (3, number_lut_nodes**3))

	return lut

if __name__ == '__main__':

	import os
	import datetime

	lut_size = 65
	display_space = 'p3'
	aces_type = 'acescct'
	lut_type = 'cube'

	dst = design_3D_lut(lut_size, display_space, aces_type, lut_type)
	print(numpy.transpose(dst))

	# lut_name = 'test_20170823'
	# time = str(datetime.datetime.now)
	# lut_min = 0
	# lut_max = 1
	# lut_1D_exists = False
	# lut_3D = dst


	# filename = os.path.join(lut_name + "." + lut_type)

	# f = open(filename, "w+")
	# f.write('# DaVinci Resolve Cube\n')
	# f.write('# Made from ' + filename + ' by Me\n')
	# f.write('# Generated on %s \n' %(datetime.datetime.now())) # + " " + datetime.time)
	# f.write('\n')
	# f.write('LUT_3D_Size ' + str(lut_size) + '\n')
	# f.write('LUT_3D_INPUT_RANGE ' + str(lut_min) + ' ' + str(lut_max)+ '\n')
	# f.write('\n')

	# if lut_1D_exists == True:
	# 	for i in range(len(lut_1D)):
	# 		f.write(str(lut_1D[i]) + '\n')
	# 	f.write('\n')

	# for i in range(lut_size**3):
	# 	f.write(str(lut_3D[0,i]) + ' ' + str(lut_3D[1,i]) + ' ' + str(lut_3D[2,i]) + '\n')



