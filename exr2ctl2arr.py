import numpy, OpenEXR, Imath, colour, create3DLUT, cv2

"""
	title::
		exr2ctl2arr

	description::
		This method takes in an image array and creates an OpenEXR file using the array and image size information. CTL render 
		is called to apply the defined ctl_transforms to the created OpenEXR file and will output a new OpenEXR file. The new 
		OpenEXR file will then be read in and expanded to find each channel of the image. The channels will then be stacked and 
		the new image array will be returned.

	attributes::
		im: image array
		im_rows: interger number of rows in the image
		im_columns: integer number of columns in the image
		ctl_transforms: path the ctl transforms; must be passed into function with brackets (if more than one transformation
			is to be applied: put the transforms in the order in which they are to be applied, seperated by a comma)

	author::
		Emily Faw
		20170726


export CTL_MODULE_PATH=/Users/emilyfaw/Source/aces-dev/transforms/ctl/lib

"""


def exr2ctl2arr(im, im_rows, im_columns, ctl_transforms):

    #creating OpenEXR file
	pixels = im.astype(numpy.float16).tostring()
	HEADER = OpenEXR.Header(im_rows, im_columns)
	half_chan = Imath.Channel(Imath.PixelType(Imath.PixelType.HALF))
	HEADER['channels'] = dict([(c, half_chan) for c in "RGB"])
	exr = OpenEXR.OutputFile("exr_in.exr", HEADER)
	exr.writePixels({'R': pixels, 'G': pixels, 'B': pixels})
	exr.close()

 #    #calling CTL Render function
	call_ctl_min = colour.utilities.ctl_render("./exr_in.exr", "./exr_out.exr", ctl_transforms)

    #opening newly formed OpenEXR file with transformed applied
	im = OpenEXR.InputFile('exr_out.exr')
	(r,g,b) = im.channels("RGB")
	dw = im.header()['dataWindow']
	size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

    #reshaping and reformating image channels to put into new array
	red = numpy.reshape(numpy.fromstring(r, dtype=numpy.float16), (size[0], size[1]))
	green = numpy.reshape(numpy.fromstring(g, dtype=numpy.float16), (size[0], size[1]))
	blue = numpy.reshape(numpy.fromstring(b, dtype=numpy.float16), (size[0], size[1]))

	image = numpy.stack((blue, green, red), axis=-1) 

	test = numpy.array(2**16)
	cv2.imwrite('cv1.tif', test)

	return image


if __name__ == '__main__':

	im = numpy.ones((3,3))
	im_rows = 3
	im_columns = 3
	ctl = "./aces_transforms/ACEScc/ACEScsc.ACEScc_to_ACES.ctl" 

	dst = exr2ctl2arr(im, im_rows, im_columns, [ctl])
	print(dst)