from image_block import *
import numpy as np
import cv2 as cv

rd = 'images.jpeg'
rd2 = 'aki_Full.jpg'

#rd.show_info()
image = cv.imread(rd)
image_1 = yuv(image)
show_info(image_1)
show_result(bgr(image_1))
image_1 = filter_yuv(image_1,np.array([[1,1,1],[1,1,1],[1,1,1]])/9)
#image_1 = remaster(image_1, levels_red=[0, 50,100,200,250], levels_green=None, levels_blue=None)
image_1 = filter_levels(image=image_1, filter_matrix=np.array([[0.5,0.5,0.5],[0.5,3,0.5],[0.5,0.5,0.5]])/7, levels={0:True,1:False,2:False})
image_1 = remaster_yuv_brightness(image_1, levels_brightness=[0,50,175,255]) 
image_1 = remaster_yuv_(image_1, levels=np.arange(0,250,15))
#image_1 = filter_levels(image=image_1, filter_matrix=np.array([[0.5,0.5,0.5],[0.5,3,0.5],[0.5,0.5,0.5]])/7, levels={0:True,1:False,2:False})
#image_1 = brightness(image_1, 255/175)
image_countur = filter_levels(copy.copy(image_1),np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]),levels={0:True,1:True,2:1})
image_countur = level2bool(image=image_countur, epsilon=20)
show_info(image_1)
show_result(bgr(image_1))
print(np.shape(image_countur))
print(image_countur[0,:])
show_result(image_countur*255)