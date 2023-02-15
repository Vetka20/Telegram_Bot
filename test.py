from bot_image import image_block as bot_image
import numpy as np
import cv2 as cv
import copy
from matplotlib import pyplot as plt


def main():

    #link to image
    rd = 'images.jpeg'
    rd2 = 'aki_Full.jpg'

    #download image 
    image = cv.imread(rd)

    #transform from BGR to YUV
    image_1 = bot_image.yuv(image)
    
    #show histogram image for analisys color
    #bot_image.show_info(image_1)
    
    #show download image
    #bot_image.show_result(bot_image.bgr(image_1))
    
    #use filter
    image_1 = bot_image.filter_yuv(image_1,np.array([[1,1,1],[1,1,1],[1,1,1]])/9)
    
    #image_1 = remaster(image_1, levels_red=[0, 50,100,200,250], levels_green=None, levels_blue=None)
    
    #use more functional filter
    #image_1 = bot_image.filter_levels(image=image_1, filter_matrix=np.array([[0.5,0.5,0.5],[0.5,3,0.5],[0.5,0.5,0.5]])/7, levels={0:True,1:False,2:False})
    
    '''
    #remaster yuv
    image_1 = bot_image.remaster_yuv_brightness(image_1, levels_brightness=[0,50,175,255]) 
    image_1 = bot_image.remaster_yuv_(image_1, levels=np.arange(0,250,15))
    '''
    #remaster yuv
    #color = [[100,100,100],[0,0,0],[255,0,0],[0,100,100],[255,100,100],[0,0,100],[100,100,0],[100,0,0],[0,100,0],[50,150,100],[50,100,150],[100,150,100],[100,100,150],[255,150,100],[255,100,150],[0,150,100],[0,150,50]]
    #color = [[0,0,0],[50,0,0],[100,0,0],[150,0,0],[0,100,0],[0,0,100],[0,100,100],[50,0,100],[50,100,0],[50,100,100],[0,150,100],[0,100,150],[50,150,100],[50,100,150],[0,200,200],[250,250,250],[250,250,100]]
    #color = [[250,0,0],[250,100,110],[250,110,100],[250,120,100],[250,100,120],[250,130,100],[250,100,130],[250,150,100],[250,100,150],[250,170,150],[250,150,170],[250,170,100],[250,100,170]]
    #color = [[128,255,0],[128,0,255],[128,128,128],[128,128,255],[128,255,128],[128,0,128],[128,128,0],[128,0,0],[128,255,255],[255,255,0],[255,0,255],[255,128,128],[255,128,255],[255,255,128],[255,0,128],[255,128,0],[255,0,0],[255,255,255],[0,255,0],[0,0,255],[0,128,128],[0,128,255],[0,255,128],[0,0,128],[0,128,0],[0,0,0],[0,255,255]]
    
    #func for create color levels
    #color = bot_image.create_color_palitra(level_brightness=[0,50,150,200,255],level_U=[0,128,255],level_V=[0,128,255])
    
    #bot_image.create_json(color=color, path="images/main", koef=[1,1,1])
    image_1 = bot_image.remaster_color_json(image=image_1, path="images/main")
    
    #image_1 = bot_image.remaster_color(image=image_1, color=color, koef=[1,1,1])
    
    
    
    
    
    #change brightness if it need
    #image_1 = bot_image.brightness(image_1, 100/250)
    
    #use filter to create contour
    image_countur = bot_image.filter_levels(copy.copy(image_1),np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]),levels={0:True,1:True,2:1})
    image_countur = bot_image.level2bool(image=image_countur, epsilon=20)
    """
    #show result histogram
    bot_image.show_info(image_1)
    
    #show result image
    bot_image.show_result(bot_image.bgr(image_1))
    
    #show result contour
    bot_image.show_result(image_countur*255)
"""
    bot_image.show_result(bot_image.bgr(image_1))
    bot_image.show_result(255-(image_countur*255))
    bot_image.show_result(bot_image.bgr(bot_image.show_palitr(color=[[255,0,255]])))
    
        
if __name__ == "__main__":
    main()