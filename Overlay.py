from PIL import Image
#import cv2
import numpy as np
import os 

def img_prep(org_image,fil_image):
   fil_image=fil_color_change(fil_image)
   org_image1 = Image.open(org_image)
   width, height = org_image1.size

   org_image_bot = org_image1.crop((0, 461, width-0, height-0))
   org_image_top = org_image1.crop((0, 0, width-0, height-461))
   fil_image_alpha = fil_image.convert("RGBA")
   org_image_alpha = org_image_bot.convert("RGBA")
   return fil_image_alpha,org_image_alpha,org_image_top


def alpha_blend(fil_image_gr, org_image_a):
	matrix = fil_image_gr.getdata()
	newData=[]
	for item in matrix:
		if item[0] < 100 and item[1] < 100 and item[2] < 100:
			newData.append((0, 0, 0, 0))
		else:
			newData.append(item)
	fil_image_gr.putdata(newData)		
	Overlay_bot  = Image.alpha_composite(org_image_a,fil_image_gr)	
	return Overlay_bot

def img_concat_v(top_half, bot_half):
	full_image = Image.new('RGB', (top_half.width, top_half.height + bot_half.height))
	full_image.paste(top_half, (0, 0))
	full_image.paste(bot_half, (0, top_half.height))
	return full_image

def fil_color_change(fil_image):
	matrix = np.array(fil_image)
	mask = np.any((matrix > [100,100,100]), axis=2)
	matrix[mask] = np.array([0,255,0])
	fil_image2 = Image.fromarray(matrix)
	return fil_image2

def bg_color_change(full_image):
	matrix = np.array(full_image)
	mask = np.any((matrix != [0,255,0]), axis=2)
	matrix[mask] = np.array([212,198,195])
	final_img = Image.fromarray(matrix)
	return final_img
"""
def a_blend(fil_image,org_image1):
	org_image_bot = fil_image.convert("RGBA")
	org_image_top = org_image1.convert("RGBA")

	alphaBlended = Image.alpha_blend(org_image_bot, org_image_top, alpha=.8)

	return alphaBlended
"""

def done(in_image):
	fil_image_gr, org_image_a,org_image_t = img_prep("frame.jpg",in_image)
	overlay_half = alpha_blend(fil_image_gr,org_image_a)
	final_img = img_concat_v(org_image_t,overlay_half)
	final_image = bg_color_change(final_img)
	return final_image
	

#in_image = Image.open("frame_0.jpg")
#done(in_image)