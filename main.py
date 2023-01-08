from image_block import *
import numpy as np
import cv2 as cv

rd = 'images.jpeg'
rd2 = 'aki_Full.jpg'

#rd.show_info()
image = cv.imread(rd)
image_1 = yuv(image)
show_info(image_1)
show_result(image_1)
image_1 = filter_yuv(image_1,np.array([[1,1,1],[1,1,1],[1,1,1]])/9)
show_info(image_1)
image_1 = remaster(image_1, levels_red=[0, 50,100,200,250], levels_green=None, levels_blue=None)
#image_1 = brightness(image_1, 255/175)
show_result(bgr(image_1))