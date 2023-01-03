from image_block import redactor

rd = redactor('aki_Full.jpg')

rd.show_info()
print(rd.original_image.shape)
rd.show_original_gray()