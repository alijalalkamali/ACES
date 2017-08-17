import numpy as np
import create3DLUT
from colour import tsplit, read_image
import cv2
import create3DLUT

"""
Processes pixels though a LUT, using trilinear interpolation.

Parameters
----------
inPixels : array_like
    Array of RGB pixels as floats in the range 0-1.
lattice : array_like
    A LUT as an (n, n, n, 3) array of floats.

Returns
-------
ndarray
"""

def lut_interpolation(im, im_type, lut_file, lut_size, interp_type):

	inPixels = read_image(im)
	# print(np.amax(inPixels))
	max_cv = np.amax(inPixels)

	lut = np.loadtxt(lut_file, skiprows=7)

	lattice = np.reshape(lut, (lut_size, lut_size, lut_size, 3), order='F')

	if interp_type == 'trilinear':
		n = lattice.shape[0] - 1
		inPixels = np.asarray(inPixels) / np.amax(inPixels)
		theShape = inPixels.shape
		inPixels = np.ravel(inPixels)
		pixels = inPixels.size/3
		inPixels = np.reshape(inPixels, (pixels, 3))
		R, G, B = tsplit(inPixels)
		rLow = np.floor(R*n).astype(np.int_)
		rHigh = np.clip(rLow + 1, 0, n)
		gLow = np.floor(G*n).astype(np.int_)
		gHigh = np.clip(gLow + 1, 0, n)
		bLow = np.floor(B*n).astype(np.int_)
		bHigh = np.clip(bLow + 1, 0, n)
		V000 = lattice[rLow, gLow, bLow]
		V001 = lattice[rLow, gLow, bHigh]
		V010 = lattice[rLow, gHigh, bLow]
		V011 = lattice[rLow, gHigh, bHigh]
		V100 = lattice[rHigh, gLow, bLow]
		V101 = lattice[rHigh, gLow, bHigh]
		V110 = lattice[rHigh, gHigh, bLow]
		V111 = lattice[rHigh, gHigh, bHigh]
		fR = n*R - rLow
		fG = n*G - gLow
		fB = n*B - bLow
		fR = np.reshape(fR, (pixels, 1))
		fG = np.reshape(fG, (pixels, 1))
		fB = np.reshape(fB, (pixels, 1))
		fR = np.tile(fR, 3)
		fG = np.tile(fG, 3)
		fB = np.tile(fB, 3)
		W000 = (1-fR)*(1-fG)*(1-fB)
		W001 = (1-fR)*(1-fG)*fB
		W010 = (1-fR)*fG*(1-fB)
		W011 = (1-fR)*fG*fB
		W100 = fR*(1-fG)*(1-fB)
		W101 = fR*(1-fG)*fB
		W110 = fR*fG*(1-fB)
		W111 = fR*fG*fB
		outPixels = V000*W000 + V001*W001 + V010*W010 + V011*W011 + V100*W100 + V101*W101 + V110*W110 + V111*W111
		outPixels = np.reshape(outPixels, theShape) * 255 * max_cv

	if interp_type == 'tetrahedral':

		n = lattice.shape[0] - 1
		inPixels = np.asarray(inPixels) / max_cv
		theShape = inPixels.shape
		inPixels = np.ravel(inPixels)
		pixels = inPixels.size/3
		inPixels = np.reshape(inPixels, (pixels, 3))
		R, G, B = tsplit(inPixels)
		rLow = np.floor(R*n).astype(np.int_)
		rHigh = np.clip(rLow + 1, 0, n)
		gLow = np.floor(G*n).astype(np.int_)
		gHigh = np.clip(gLow + 1, 0, n)
		bLow = np.floor(B*n).astype(np.int_)
		bHigh = np.clip(bLow + 1, 0, n)
		V000 = lattice[rLow, gLow, bLow]
		V001 = lattice[rLow, gLow, bHigh]
		V010 = lattice[rLow, gHigh, bLow]
		V011 = lattice[rLow, gHigh, bHigh]
		V100 = lattice[rHigh, gLow, bLow]
		V101 = lattice[rHigh, gLow, bHigh]
		V110 = lattice[rHigh, gHigh, bLow]
		V111 = lattice[rHigh, gHigh, bHigh]
		fR = n*R - rLow
		fG = n*G - gLow
		fB = n*B - bLow
		fR = np.reshape(fR, (pixels, 1))
		fG = np.reshape(fG, (pixels, 1))
		fB = np.reshape(fB, (pixels, 1))

		outPixels = (1-fG)*V000 + (fG-fR)*V010 + (fR-fB)*V110 + fB*V111
		outPixels = np.where(np.logical_and(fR>fG, fG>fB), (1-fR)*V000 + (fR-fG)*V100 + (fG-fB)*V110 + fB*V111, outPixels)
		outPixels = np.where(np.logical_and(fR>fG, fR>fB), (1-fR)*V000 + (fR-fB)*V100 + (fB-fG)*V101 + fG*V111, outPixels)
		outPixels = np.where(np.logical_and(fR>fG, fB>=fR), (1-fB)*V000 + (fB-fR)*V001 + (fR-fG)*V101 + fG*V111, outPixels)
		outPixels = np.where(np.logical_and(fG>=fR, fB>fG), (1-fB)*V000 + (fB-fG)*V001 + (fG-fR)*V011 + fR*V111, outPixels)
		outPixels = np.where(np.logical_and(fG>=fR, fB>fR), (1-fG)*V000 + (fG-fB)*V010 + (fB-fR)*V011 + fR*V111, outPixels)
		outPixels = np.clip(outPixels, 0., np.inf)

		outPixels = np.reshape(outPixels, theShape) * 255 * max_cv
    # return outPixels

	# print(outPixels)
	cv2.imwrite('test_tetrahedral.tiff', outPixels.astype(np.uint8))

	return outPixels


if __name__ == '__main__':

	# im = '/Users/oscar/Desktop/Emily/aces_app/test.tiff'
	im = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/sample_images/aces.0144.exr'
	# im = '/Users/oscar/Desktop/Emily/aces_app/BatteryPark_aces.exr'
	# im_type = 'tiff'
	im_type = 'exr'
	lut_file = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/test.cube'
	lut_size = 65

	dst = lut_interpolation(im, im_type, lut_file, lut_size, 'tetrahedral')





