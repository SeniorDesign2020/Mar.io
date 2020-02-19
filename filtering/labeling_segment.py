import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

input_file = input('input filename\n')
num_images =  len([f for f in os.listdir(input_file)if os.path.isfile(os.path.join(input_file, f))])
output_file = 'filtered_images'

try:
    os.mkdir(output_file)
except OSError:
    print ("Creation of the directory {} failed".format(output_file))
print(num_images)
for i in range(num_images):
    img  = cv2.imread('{}/frame{}.jpg'.format(input_file,i))
    shape = np.shape(img)
    height = int(shape[0]/2)
    cropped = img[height:shape[0],:]
    img=cv2.cvtColor(cropped,cv2.COLOR_BGR2RGB)
    vectorized = img.reshape((-1,3))
    vectorized = np.float32(vectorized)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 2
    attempts=10
    ret,label,center=cv2.kmeans(vectorized,K,None,criteria,attempts,cv2.KMEANS_PP_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    result_image = res.reshape((img.shape))
    figure_size = 15

    dst = cv2.medianBlur(result_image,35)

    cv2.imwrite('{}/frame_{}.jpg'.format(output_file,i),dst)
