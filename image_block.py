import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt 

class redactor():
    
    def __init__(self,src) -> None:
        self.image = cv.imread(src)
        self.size = len(self.image)

    
    def set_filter_parametr(self) -> None:
        
        
        pass
    
    def show_info(self) -> None:
        plt.figure()
        plt.hist(self.image[0])
        
        


    def filter() -> list:
        
        pass