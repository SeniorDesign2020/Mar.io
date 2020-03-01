import os 
import boto3
from labeling_segment import filtering as fil
from Overlay import done
import cv2
from PIL import Image
from tqdm import tqdm
import shutil
from copy import deepcopy
video_name =  input('video_name\n')
folder_name = input('folder_name\n')
keys = []
bucket = 'senior-design33'


destination = 'LabelledFrames'
if os.path.isfile('aws.txt'):
    with open('aws.txt','r') as in_file:
        line = in_file.readline()
        line=line.strip()
        ACCESS_KEY = line
        line = in_file.readline()
        line=line.strip()
        SECRET_KEY = line
else:
    ACCESS_KEY = input('access_key\n')
    keys.append(ACCESS_KEY)
    SECRET_KEY = input('secret_key\n')
    keys.append(SECRET_KEY)
    with open('aws.txt','w') as out_file:
        for line in keys:
            out_file.write(line)
            out_file.write("\n")

os.mkdir('{}'.format(folder_name))

s3_client = boto3.client('s3',aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
paginator = s3_client.get_paginator('list_objects')
operation_parameters = {'Bucket': bucket,
                        'Prefix': 'Frames/{}/{}'.format(video_name, folder_name)}
pages = paginator.paginate(**operation_parameters)

for page in pages:
    for obj in tqdm(page['Contents']):
        frame_number = obj['Key'].split('/')[-1]
        s3_client.download_file('senior-design33',obj['Key'],'frame.jpg')
        try:
            filtered_image = fil('frame.jpg')
            image_cv2 = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_cv2)
            
            image_label=done(image_pil)
            image_label.save('{}/{}'.format(folder_name,frame_number))
        except:
            key = s3_client.lookup(obj['Key'])
            if key.size <=0:
                s3_client.delete_object(Bucket=bucket,Key=obj['Key'])
            else:
                print('Cant label the frame {} \n Skipping for now'.format(frame_number))
            
        

shutil.make_archive('{}'.format(folder_name),'zip','{}'.format(folder_name))
print('Uploading...')
s3_client.upload_file('{}.zip'.format(folder_name), bucket, 'LabelledFrames/{}/{}.zip'.format(video_name,folder_name))    
shutil.rmtree('{}'.format(folder_name))
os.remove('{}.zip'.format(folder_name))        
