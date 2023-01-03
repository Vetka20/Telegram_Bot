import cv2 as cv

import numpy as np
import matplotlib.pyplot as plt 

class redactor():
    
    def __init__(self,src) -> None:
        self.original_image = np.array(cv.imread(src))
        #self.size = self.original_image.size()
        self.original_gray_image = cv.cvtColor(self.original_image, cv.COLOR_BGR2GRAY)
        

    def __raskladka(self):
        result =[[],[],[]]
        for i in self.original_image[:,:,0]:
            result[0].extend(i)
        for i in self.original_image[:,:,1]:
            result[1].extend(i)
        for i in self.original_image[:,:,2]:
            result[2].extend(i)
        return np.array(result)    

    def show_original(self):
        cv.imshow("Display window", self.original_image)
        cv.waitKey(0)
        
    def show_original_gray(self):
        cv.imshow("Display window", self.original_gray_image)
        cv.waitKey(0)
    
    def set_filter_parametr(self, *args) -> None:
        self.filter = np.array(args)
    
        
    
    def show_info(self) -> None:
        plt.figure()
        plt.subplot(3,1,1)
        plt.hist(self.__raskladka()[0], bins=25)
        plt.subplot(3,1,2)
        plt.hist(self.__raskladka()[1], bins=25)
        plt.subplot(3,1,3)
        plt.hist(self.__raskladka()[2], bins=25)
        plt.show()
        


    def filter() -> list:
        
        pass