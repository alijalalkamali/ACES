import numpy, OpenEXR, create3DLUT
from colour import read_image

"""

	title: 
		unpack_exr

	description: 
		This method takes in an OpenEXR image file, unpacks it, and returns a 3D array of the red,
		green, and blue channels of the image with the correct image dimensions. If the .exr file
		is not ACES standards, a warning and/or error will be rasied.

	attributes: 
		exr_image: the input OpenEXR image file
		bit_depth: bit depth of image (default is 16 by standard)

	author:
		Emily Faw
		20170705

"""

def unpack_exr(exr_image, bit_depth=16):

    #open the EXR file using OpenEXR python wrapper
	im = OpenEXR.InputFile(exr_image)

	try:
		str(im.header()['acesImageContainerFlag'])
	except KeyError:
		print('EXR file does not contain ACES container flag and therefore does not meet the SMPTE standards')

    #ACES Chromaticities
    #if the file does not contain the correct red, green, blue, and white point chromaticities, 
    #   then the EXR file is not an ACES file and cannot continue
	if str(im.header()['chromaticities'].red) != '(0.7347000241279602, 0.2653000056743622)':
		print('ERROR')
		raise ValueError('Red Chromaticities are bad')
	if str(im.header()['chromaticities'].green) != '(0.0, 1.0)':	
		raise ValueError('Green Chromaticities are bad')
	if str(im.header()['chromaticities'].blue) != '(9.999999747378752e-05, -0.07699999958276749)':
		raise ValueError('Blue Chromaticities are bad')
	if str(im.header()['chromaticities'].white) != '(0.3216800093650818, 0.3376699984073639)':		
		raise ValueError(' White point Chromaticities are bad')

    #if file is an ACES EXR file, the find the red, green, and blue channels from the image
	(r,g,b) = im.channels("RGB")

    #find the image size information from the header
	dw = im.header()['dataWindow']
	size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

    #extract the red, green, and blue color record, change to floating point number and 
    #    reshape to the size of the image
	red = numpy.reshape(numpy.fromstring(r, dtype=numpy.float16), (size[1],size[0]))
	green = numpy.reshape(numpy.fromstring(g, dtype=numpy.float16), (size[1], size[0]))
	blue = numpy.reshape(numpy.fromstring(b, dtype=numpy.float16), (size[1], size[0]))


    #stack the red, green, and blue record to create the image array
	image = numpy.stack((red, green, blue), axis=-1)

	image_io = read_image(exr_image)

	return image, image_io 


if __name__ == '__main__':

	import numpy
	import OpenEXR
	import cv2

	exr_im = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/sample_images/aces.0144.exr'
	# exr_im = 'BatteryPark_aces.exr'

	image_bands, image_io = unpack_exr(exr_im, 16)
	print('openexr', image_bands)
	print('image io', image_io)

	#cv2.imwrite('test.tiff', image_bands.astype(numpy.uint16))
	# new_exr_im = OpenEXR.OutputFile("test_exr.exr", OpenEXR.Header(size[1],size[0]))
	# exr_im.writePixels({'R' : red.tostring(), 'G' : green.tostring(), 'B' : blue.tostring()})



