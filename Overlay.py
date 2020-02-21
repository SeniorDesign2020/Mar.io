from PIL import Image
#import cv2
import numpy as np
import os 
"""
 Function to change the image size
def changeImageSize(maxWidth, 
                    maxHeight, 
                    image):
    
    widthRatio  = maxWidth/image.size[0]
    heightRatio = maxHeight/image.size[1]
    newWidth    = int(widthRatio*image.size[0])
    newHeight   = int(heightRatio*image.size[1])
    newImage    = image.resize((newWidth, newHeight))
    return newImage
"""   

def img_prep(path1,path2):
   image1= Image.open(path2)
   image1=change(image1)
   image2 = Image.open(path1)
   #Image size
   width, height = image2.size
   #print(height,width)

   image3 = image2.crop((0, 461, width-0, height-0))
   image4 = image2.crop((0, 0, width-0, height-461))
   image7 = image1.convert("RGBA")
   image8 = image3.convert("RGBA")
   return image7,image8,image4


def blend(img1, img2):
	datas = img1.getdata()
	newData=[]
	for item in datas:
	#print(item)
		if item[0] < 100 and item[1] < 100 and item[2] < 100:
			newData.append((0, 0, 0, 0))
		else:
			newData.append(item)
		
	img1.putdata(newData)		
	Blend1  = Image.alpha_composite(img2,img1)	
	return Blend1

def get_concat_v(im1, im2):
	dst = Image.new('RGB', (im1.width, im1.height + im2.height))
	dst.paste(im1, (0, 0))
	dst.paste(im2, (0, im1.height))
	return dst

def change(im3):
	matrix = np.array(im3)
	#mask1 = np.any((matrix != [126,128,151]), axis=2)
	#mask2 = np.any((matrix == [126,128,151]) | (matrix == [119,171,141]) | (matrix == [131,133,158]), axis=2)
	mask3 = np.any((matrix > [100,100,100]), axis=2)
	#matrix[np.where((matrix == [126,128,151]).all(axis=2))]=[119,251,0]
	matrix[mask3] = np.array([0,255,0])
	im = Image.fromarray(matrix)
	#im.save("final.png")
	#im.show()
	return im

def change_2(im4):
	matrix1 = np.array(im4)
	#mask1 = np.any((matrix != [126,128,151]), axis=2)
	#mask2 = np.any((matrix == [126,128,151]) | (matrix == [119,171,141]) | (matrix == [131,133,158]), axis=2)
	mask3 = np.any((matrix1 != [0,255,0]), axis=2)
	#matrix[np.where((matrix == [126,128,151]).all(axis=2))]=[119,251,0]
	matrix1[mask3] = np.array([212,198,195])
	im1 = Image.fromarray(matrix1)
	#im.save("final.png")
	#im.show()
	return im1

def a_blend(image1,image2):
	image3 = image1.convert("RGBA")
	image4 = image2.convert("RGBA")

	alphaBlended = Image.blend(image3, image4, alpha=.8)

	return alphaBlended



"""
img1, img2,img3 = img_prep()
img_blend = blend(img1,img2)
#im_f = get_concat_v(image4,alphaBlended2)
img_final = get_concat_v(img3,img_blend)
img_final = change_2(img_final)
#final image
#img_final.save("frame82.png")
plz = Image.open("frame82.JPG")
final_image = a_blend(plz,img_final)
final_image.show()
final_image.save("frame82.png")
#(im)
#matrix[np.where((matrix == [126,128,151]).all(axis=2))]=[119,251,0]
"""

def done():
		
	img1, img2,img3 = img_prep("frame.jpg","fil_image.jpg")
	img_blend = blend(img1,img2)
	img_final = get_concat_v(img3,img_blend)
	img_final = change_2(img_final)
	#final image
	#img_final.save("frame82.png")
	#work = Image.open("frame82.JPG")
	#final_image = a_blend(work,img_final)
	#final_image.show()
	#final_image.save("frame82.png")
	return img_final
	#img_final.show()
