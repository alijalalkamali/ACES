### ACES VIEWER

import create3DLUT, cv2
from colour import write_image, read_image
import time

start = time.clock()

#define input image
im = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/sample_images/aces.0144.exr'

#unpack exr image using unpack_exr
# input_im = create3DLUT.unpack_exr(im)
input_im = read_image(im)


#define lut file
lut_file = '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/create3DLUT/test_20170809.cube'

#run image through interpolation with corresponding lut
im_interp = create3DLUT.lut_interpolation(im, 'tiff', lut_file, 65, 'trilinear')

#write out image file
cv2.imwrite('filename.tiff', im_interp)

#display image to viewer with warning message about color spaces

elapsed = (time.clock() - start)
print('elapsed time', elapsed)

