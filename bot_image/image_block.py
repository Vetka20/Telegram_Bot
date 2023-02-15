import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt 
import copy
from threading import Thread 
import asyncio
from functools import lru_cache
import json


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
            
def remaster_yuv_brightness(image):
    max_brightness = np.max(image[:,:,0])
    print(f"Max brightness: {max_brightness}")
    if max_brightness == 255:
        return image
    k = 255/max_brightness
    for i in image:
        for j in i:
            j[0] = j[0]*k
                
    return image



def remaster_yuv_(image:list ,levels: list[int]):
    for i in image:
        for j in i:
            for k in reversed(levels):
                if j[1] > k: 
                    j[1] = k
                    break
            for l in reversed(levels):
                if j[2] > l: 
                    j[2] = l
                    break
    return image

def create_color_palitra(level_brightness:list[int], level_U:list[int], level_V:list[int]):
    result = []
    level_brightness = list(set(level_brightness))
    level_U = list(set(level_U))
    level_V = list(set(level_V))
    for i in level_brightness:
        for j in level_U:
            for k in level_V:
                result.append([i,j,k])    
    return result



def remaster_color(image:np.array, color:list[list[int]], koef:list[float]=[1,1,1]) -> np.array : 
    
    for i in image:
        for j in i:
            j_copy = cache_function(tuple(j), koef=tuple(koef))
            j[0] = copy.deepcopy(j_copy[0])
            j[1] = copy.deepcopy(j_copy[1])
            j[2] = copy.deepcopy(j_copy[2])
    print(f"type i: {type(i)},   size i: {np.size(i)}")
    print(f"type j:  {type(j)},  size j: {np.size(j)}") 
    print(f"len color: {len(color)}")       
    return image
                
            
    

def show_result(img, title="Display window"):
    cv.imshow(title, img)
    cv.waitKey(0)



def filter(gray_image, filter_matrix) -> list:
    return cv.filter2D(gray_image, ddepth=-1, kernel=filter_matrix)

def filter_yuv(image, filter_matrix):
    image[:,:,1] = cv.filter2D(image[:,:,1], ddepth=-1, kernel=filter_matrix)
    image[:,:,2] = cv.filter2D(image[:,:,2], ddepth=-1, kernel=filter_matrix)
    
    return image

def filter_levels(image:list[list[int]]=None, filter_matrix:list[list[float]]= [[1,1,1],[1,1,1],[1,1,1]], levels:dict[int:bool]={0:1,1:1,2:1}, dst=None):
    if dst != None:
        image = cv.imread(f"{dst}/buffer.jpg")
    filter_matrix = np.array(filter_matrix)
    filter_matrix = filter_matrix/filter_matrix.sum()
    #filter_matrix = filter_matrix/filter_matrix.count()
    for k,v in levels.items():
        if (k < 0) or (k>2):
            print("Invalid level of image. Example : levels=dict[0:False, 1:True, 2:True]/ Недопустимое значение для слоя изображения. Пример: levels=dict[0:False, 1:True, 2:True]")
        if v:
            image[:,:,k] = cv.filter2D(image[:,:,k], ddepth=-1, kernel=filter_matrix)
    
    if dst != None:
        cv.imwrite(f"{dst}/result.jpg", image)
        return
    return image

def brightness(image, k):
    image[:,:,0]=image[:,:,0]*k
    image[:,:,1]=image[:,:,1]*k
    image[:,:,2]=image[:,:,2]*k 
    return image

def countur(image:list[list]):
    pass

def level2bool(image, epsilon):
    
    image = np.array(image)
    result = np.zeros_like(image[:,:,0])
    image.astype(np.bool_)
    result = result + image.astype(np.bool_)[:,:,0] + image.astype(np.bool_)[:,:,1] +image.astype(np.bool_)[:,:,2]
    return result

def correct(src_image, id):
    image = cv.imread(src_image)
    image_1 = yuv(image)
    image_1 = remaster_yuv_brightness(image=image_1)
    color = create_color_palitra(level_brightness=[0,32,64,96,128,160,192,224,255] ,level_U=[0,32,64,96,128,160,192,224,255] ,level_V=[0,32,64,96,128,160,192,224,255] )#[0,32,64,96,128,160,192,224,255] 
    image_1 = remaster_color(image=image_1, color=color, koef=[1,1,1])
    image_1 = cv.cvtColor(image_1, cv.COLOR_YUV2BGR)
    cv.imwrite(f"/home/vetka/Telegram_Bot/images/{id}/result.jpg", image_1)
    image_countur = filter_levels(copy.copy(image_1),np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]]),levels={0:True,1:True,2:True})
    image_countur = level2bool(image=image_countur, epsilon=20)
    image_countur = 255-(image_countur*255)
    cv.imwrite(f"/home/vetka/Telegram_Bot/images/{id}/result_countur.jpg", image_countur)

def show_palitr(color:list[list[int]], koef: list[int] = [1,1,1]):
    image = np.zeros((600,800,3), np.uint8)
    weight_rec = int(800/len(color))
    for i in range(0,len(color)):
        cv.rectangle(img=image, pt1=[i*weight_rec,0], pt2=[(i+1)*weight_rec,300], color=color[i], thickness=-1)
    for j in range(0,1):
        for k in range(0,255):
            for l in range(0,255):
                #cv.rectangle(img=image, pt1=[l+300,k+300], pt2=[l,j], color=[j,k,l], thickness=-1)
                pass
        print(f"{j/2.55}%")        
    return image

def remaster_color_tread(image:np.array, color:list[list[int]], koef:list[float]=[1,1,1]):
    for i in image:
        
        threads = [Thread(target=_image_thread, args=(j,tuple(koef))) for j in i]
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()

    
    return image



def _image_thread(j:np.array, color:list[list[int]], koef:list[float]=[1,1,1]):
    
    j_copy = cache_function(j=tuple(j), koef=tuple(koef))
    j[0] = copy.deepcopy(j_copy[0])
    j[1] = copy.deepcopy(j_copy[1])
    j[2] = copy.deepcopy(j_copy[2])


@lru_cache(maxsize=None)
def cache_function(j, koef):
    color = create_color_palitra(level_brightness=[0,32,64,96,128,160,192,224,255],level_U=[0,32,64,96,128,160,192,224,255],level_V=[0,32,64,96,128,160,192,224,255])
    min = 10000
    for k in range(0,len(color)):
        bufer = abs(koef[0]*(j[0]-color[k][0]))+abs(koef[1]*(j[1]-color[k][1]))**2+abs(koef[2]*(j[2]-color[k][2]))**2
        if bufer < min:
            """j[0] = copy.deepcopy(color[k][0])
            j[1] = copy.deepcopy(color[k][1])
            j[2] = copy.deepcopy(color[k][2])
            """
            j_copy = color[k]
            min = copy.deepcopy(bufer)
    return j_copy

def create_json(color, path, koef=[1,1,1]):
    result_dict = {}
    

    for i in range(0,256):
        result_dict[i] = {}
        for j in range(0,256):
            result_dict[i][j]={}
            for w in range(0,256):
                min = 10000
                for k in range(0,len(color)):
                    bufer = abs(koef[0]*(i-color[k][0]))+abs(koef[1]*(j-color[k][1]))**2+abs(koef[2]*(w-color[k][2]))**2
                    if bufer < min:
                        """j[0] = copy.deepcopy(color[k][0])
                        j[1] = copy.deepcopy(color[k][1])
                        j[2] = copy.deepcopy(color[k][2])
                        """
                        j_copy = color[k]
                        min = copy.deepcopy(bufer)
                result_dict[i][j][w] = j_copy
        print(f"{i}/255")
    with open(f"/{path}/json_palitr.json", "w") as outfile:
        json.dump(result_dict ,outfile)

def remaster_color_json(image, path):
    with open(f"{path}/json_palitr.json", "r") as openfile:
        color_dict = json.load(openfile)
    for i in image:
        for j in i:
            j = color_dict[str(j[0])][str(j[1])][str(j[2])]
    return image

def save(dst_from: str, dst_to:str):
    """Save image from "dst_from" to "dst_to" need for resave image"""
    image = cv.imread(dst_from)
    cv.imwrite(dst_to, image)

def hist(image_level, levels):
    
    H,bin = np.histogram(image_level, levels)
    return H,bin

def full_diagram(color, image=None, dst=None):
    if image ==None:
        image = cv.imread(dst)
    return hist(image[:,:,0], color)
