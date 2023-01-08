import cv2 as cv
import copy
import numpy as np
import matplotlib.pyplot as plt 

#__all__ = [show_info, gray]



def gray(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

def yuv(image):
    return cv.cvtColor(image, cv.COLOR_BGR2YUV)

def bgr(image):
    return cv.cvtColor(image, cv.COLOR_YUV2BGR)

def __raskladka(image):
    result =[[],[],[]]
    for i in image[:,:,0]:
        result[0].extend(i)
    for i in image[:,:,1]:
        result[1].extend(i)
    for i in image[:,:,2]:
        result[2].extend(i)
    return np.array(result)    



def set_filter_parametr(self, matrix) -> None:
    self.filter_parametrs = np.array(matrix)

    

def show_info(image) -> None:
    plt.figure()
    plt.subplot(3,1,1)
    plt.hist(__raskladka(image)[0], bins=25)
    plt.subplot(3,1,2)
    plt.hist(__raskladka(image)[1], bins=25)
    plt.subplot(3,1,3)
    plt.hist(__raskladka(image)[2], bins=25)
    plt.show()
    
def remaster(image, levels_red, levels_green=None, levels_blue=None):
    if levels_green == None:
        levels_green = levels_red
    if levels_blue == None:
        levels_blue = levels_red
    
    for i in image:
        for j in i:
            for k in reversed(levels_red):
                if j[2] > k: 
                    j[2] = k
                    break
            for l in reversed(levels_green):
                if j[1] > l: 
                    j[1] = l
                    break
            for m in reversed(levels_blue):
                if j[0] > m: 
                    j[0] = m
                    break
    return image
            
def remaster_yuv(image, levels_brightness):
    pass

def show_result(img, title="Display window"):
    cv.imshow(title, img)
    cv.waitKey(0)



def filter(gray_image, filter_matrix) -> list:
    return cv.filter2D(gray_image, ddepth=-1, kernel=filter_matrix)

def filter_yuv(image, filter_matrix):
    image[:,:,1] = cv.filter2D(image[:,:,1], ddepth=-1, kernel=filter_matrix)
    image[:,:,2] = cv.filter2D(image[:,:,2], ddepth=-1, kernel=filter_matrix)
    
    return image
    

def brightness(image, k):
    image[:,:,0]=image[:,:,0]*k
    image[:,:,1]=image[:,:,1]*k
    image[:,:,2]=image[:,:,2]*k 
    return image
    