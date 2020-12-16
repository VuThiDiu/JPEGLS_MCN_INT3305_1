import os
from PIL import Image
import numpy as np
from Encode import JPEGLSEncode
import cv2
from TestEncoding import *


def read(fp):
    """Read image data from file-like object using PIL.  Return Numpy array.
    """
    with open(fp, 'rb') as fpp:
        img = PIL.Image.open(fpp).convert('LA')
        data = np.asarray(img)

    return data



def write(fp, data, fmt=None, **kwargs):
    """Write image data from Numpy array to file-like object.

    File format is automatically determined from fp if it's a filename, otherwise you
    must specify format via fmt keyword, e.g. fmt = 'png'.

    Parameter options: http://pillow.readthedocs.io/en/4.2.x/handbook/image-file-formats.html
    """
    img = PIL.Image.fromarray(data)
    img.save(fp, format=fmt, **kwargs)


# Read in an image from an existing PNG file.
img = Image.open('bee.png').convert('LA')
img.save('bee.png')
img =  cv2.imread('bee.png')
img = cv2.resize(img, (600, 400))
cv2.imshow('Image Test', img)
cv2.waitKey(0)
dataImage = np.asarray(img)
dataImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
example =  JPEGLSEncode()
data_buffer = example.Encode(dataImage)
# print(data_buffer)
# test = TestEncoding()
# test_str = test.Result8()
# data_buffer = example.Encode([[0,0,90,74],[68,50,43,205], [64,145,145,145], [100,145,145,145]])
# for x in range(len(test_str)):
#     if (data_buffer[x] == test_str[x]):
#         print("True")
#     else: print("No")
    

# print(data_buffer)






# fname_img = 'bee.png'
# data_image = read(fname_img)


# image = cv2.imread('bee.png')
# image = cv2.resize(image, (600, 400))

# cv2.imshow('image', image)
# cv2.waitKey(0)
# print(np.asarray(image))

# data_image = np.asarray(image)
# data_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# print(data_image.shape)

# # This input image should be a numpy array.
print('\nData properties:')
print('Type:  {:s}'.format(str(dataImage.dtype)))
print('Shape: {:s}'.format(str(dataImage.shape)))

# # # Compress image data to a sequence of bytes.
# data_buffer = JPEGLSEncode.Encode(data_image)


print('\nSize of uncompressed image data: {:n}'.format(len(dataImage.tobytes())))
print('Size of JPEG-LS encoded data:    {:n}'.format(len(data_buffer)))

# # # Decompress.
# # data_image_b = jpeg_ls.decode(data_buffer)

# # # Compare image data, before and after.
# # is_same = (data_image == data_image_b).all()
# # print('\nRestored data is identical to original? {:s}\n'.format(str(is_same)))

# # cv2.imshow('Origin', data_image)
# # cv2.imshow('After encode and decode', data_image_b)
# # cv2.waitKey(0)