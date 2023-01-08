from image_block import *
import numpy as np
import cv2 as cv

rd = 'images.jpeg'
rd2 = 'aki_Full.jpg'

#rd.show_info()
image = cv.imread(rd)
show_info(image)
image_1 = remaster(image, levels_red=[20, 50,255], levels_green=[0,50,150,255], levels_blue=[0,50,100,150,255])
show_result(image_1)