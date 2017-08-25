import numpy, create3DLUT, cv2
# from resizeimage import resizeimage

"""
	title::
		build_3D_lut

	description::
		This method builds a 3D Look Up Table (LUT) from a minimum value, maximum value, and the specified size of the lut
			using numpy functions. 

	attributes::
		lut_min: minimum value for 3D lut
		lut_max: maximum value for 3D lut
		number_nodes: the number of nodes in lut (17,33,65); will result in lut the size of  number_nodes^3
		fast_channel: 'blue' or 'red' to indicate which channel is "fast"

	author::
		Emily Faw
		20170727

"""

def build_3D_lut(lut_min, lut_max, number_nodes, fast_channel):

	lut_3d_nodes = numpy.reshape(numpy.linspace(lut_min, lut_max, number_nodes), (1, number_nodes))
	cube = numpy.transpose(numpy.zeros((number_nodes**3, 3)))

    # resize each channel differently to create every combination of lut nodes, sort to get the values in numerical order, repmat two channels to 
    # 	the length of the lut
	if fast_channel == 'red':
		cube[2,:] = numpy.sort(numpy.resize(lut_3d_nodes, (1, number_nodes**3)))
		cube[1,:] = numpy.matlib.repmat(numpy.sort(numpy.resize(lut_3d_nodes, (1, number_nodes**2))), 1, number_nodes)
		cube[0,:] = numpy.matlib.repmat(numpy.sort(numpy.resize(lut_3d_nodes, (1, number_nodes))), 1, number_nodes**2)

	if fast_channel == 'blue':
		cube[0,:] = numpy.sort(numpy.resize(lut_3d_nodes, (1, number_nodes**3)))
		cube[1,:] = numpy.matlib.repmat(numpy.sort(numpy.resize(lut_3d_nodes, (1, number_nodes**2))), 1, number_nodes)
		cube[2,:] = numpy.matlib.repmat(numpy.sort(numpy.resize(lut_3d_nodes, (1, number_nodes))), 1, number_nodes**2)

	the_cube = numpy.transpose(cube)
	return the_cube


if __name__ == '__main__':

	lut_min = 0
	lut_max = 1
	number_nodes = 3
	fast_channel = 'blue'

	dst = build_3D_lut(lut_min, lut_max, number_nodes, fast_channel)
	print(dst.shape)
	print(dst)
