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

def unpack_exr(exr_image):

	image_io = read_image(exr_image)

	return image_io 


if __name__ == '__main__':

	import numpy
	import OpenEXR
	import cv2

	exr_im = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/sample_images/aces.0144.exr'
	# exr_im = 'BatteryPark_aces.exr'

	image_io = unpack_exr(exr_im, 16)