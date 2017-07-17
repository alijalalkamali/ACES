import numpy

"""

	title: 
		extract_LUT

	description: 
		This method takes in a LUT file of either (cube/Resolve, cub/Filmlight, xml/cfl/AMPAS)
		and extracts the 3D LUT and 1D LUT if available. 

	attributes: 
		LUT_file: the LUT file
		LUT_type: the type of LUT file (cube, cub, cfl)
		LUT_1D: True if the LUT file includes a 1D LUT and False if the LUT file does not include 
			a 1D file.

	author:
		Emily Faw
		20170710

"""


def extract_LUT(LUT_file, LUT_type, LUT_1d=True):

#########Resolve
	if LUT_type == 'cube': 

		f = open(LUT_file,'r')
		text = f.readline()
		x = []
		for line in f.readlines():
			y = [value for value in line.split()]
			x.append(y)
		f.close()

		#do not want first 7 arrays
		lut_arr = x[6:]
		red = []
		green = []
		blue = []
		for i in range(len(lut_arr)):
			r,g,b = float(lut_arr[i][0]), float(lut_arr[i][1]), float(lut_arr[i][2])
			red.append(r)
			green.append(g)
			blue.append(b)

		rgb_lut_3d = numpy.stack((blue, green, red), axis=-1)
		print(rgb_lut)

		#header information
		lut_size = float(x[3][1])
		lut_min = float(x[4][1])
		lut_max = float(x[4][2])
		print(lut_max, lut_min, lut_size)

#############filmlight
	if LUT_type == 'cub':

		lut1 = []
		inputLut = []
		cubeLut = []

		with open(LUT_file) as f:
			for line in f:

				if '# inGamut' in line:
					for line in f:
						if not line.strip():
							break
						else:
							lut1.append(float(line.strip()))
				if '# InputLUT' in line:
					for line in f:
						if not line.strip():
							break
						else:
							inputLut.append([float(l) for l in line.strip().split('	')])
				if '# Cube' in line:
					for line in f:
						if not line.strip():
							break
						else:
							cubeLut.append([float(l) for l in line.strip().split('	')])

		#inGamut_lut_1d = numpy.array(lut1)
		rgb_lut_1d = numpy.array(lut1)
		input_lut_3d = numpy.array(inputLut)
		rgb_lut_3d = numpy.array(cubeLut)

		

########## if LUT_type == '.clf': #maybe .xml Academy Common LUT format
	if LUT_type == 'clf':

		with open(LUT_file) as f:
			for line in f:

				lut_1d = []
				lut_3d = []

				if '<LUT1D' in line:
					f.next()
					for line in f:
						if '</Array' in line:
							for line in f:
								if '<LUT3D' in line:
									f.next()
									for line in f:
										if '</Array' in line:
											break
										lut_3d.append(line.strip('\t').strip('\n').strip().split('     '))
						if '</Process' in line:
							break
						lut_1d.append(line.strip('\n').strip().split('     '))
		red1 = []
		green1 = []
		blue1 = []

		for i in range(len(lut_1d)):
			r1,g1,b1 = float(lut_1d[i][0]), float(lut_1d[i][1]), float(lut_1d[i][2])
			red1.append(r1)
			green1.append(g1)
			blue1.append(b1)
		rgb_lut_1d = numpy.transpose(numpy.array((red1, green1, blue1)))

		red3 = []
		green3 = []
		blue3 = []

		for i in range(len(lut_3d)):
			r3,g3,b3 = float(lut_3d[i][0]), float(lut_3d[i][1]), float(lut_3d[i][2])
			red3.append(r3)
			green3.append(g3)
			blue3.append(b3)
		rgb_lut_3d = numpy.transpose(numpy.array((red3, green3, blue3)))
			
		print('1D', rgb_lut_1d.shape, '3D', rgb_lut_3d.shape)


	return rgb_lut_3d, rgb_lut_1d


	# if LUT_type == '.csp': #CineSpace/RV


if __name__ == '__main__':


	lut_3d, lut_1d = extract_LUT('LMT Kodak 2383 Print Emulation (1).xml', 'clf', LUT_1d=True)
