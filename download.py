import os 
import boto3
from labeling_segment import filtering as fil
from Overlay import done
import cv2
from PIL import Image
filename =  input('video_name\n')
folder_name = input('folder_name\n')
keys = []
bucket = 'senior-design33'

destination = 'LabelledFrames'
if os.path.isfile('aws.txt'):
    with open('aws.txt','r') as in_file:
        line = in_file.readline()
        ACCESS_KEY = line
        line = in_file.readline()
        print(line)
        SECRET_KEY = line
else:
    ACCESS_KEY = input('acces_key\n')
    keys.append(ACCESS_KEY)
    SECRET_KEY = input('secrete_key\n')
    keys.append(SECRET_KEY)
    with open('aws.txt','w') as out_file:
        for line in keys:
            out_file.write(line)
            out_file.write("\n")
            

s3_client = boto3.client('s3',aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)

paginator = s3_client.get_paginator('list_objects')
operation_parameters = {'Bucket': bucket,
                        'Prefix': 'Frames/{}/{}'.format(filename,folder_name)}
pages = paginator.paginate(**operation_parameters)
for page in pages:
    for obj in page['Contents']:
        frame_number = obj['Key'].split('/')[-1]

        s3_client.download_file('senior-design33',obj['Key'],'frame.jpg')
        
        filtered_image = fil('frame.jpg')
        cv2.imwrite('fil_image.jpg',filtered_image)
        labelled_image = done()
        #cv2.imwrite('fil_image.jpg',filtered_image)
        labelled_image.save("labelled_image.jpg")
        s3_client.upload_file('labelled_image.jpg',bucket,'LabelledFrames/{}/{}/{}'.format(filename,folder_name,frame_number))
            
        
        
'''
os.mkdir('frames')    
bucket = 'senior-design33'
client = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
response = client.list_objects_v2(
            Bucket=bucket,
            Prefix ='Frames/{}'.format(filename),
            MaxKeys=100 )

for i,obj in enumerate(response['Contents']):
    frame_number = obj['Key'].split('/')[-1]
    
    client.download_file(bucket, obj['Key'], 'frames/{}'.format(frame_number))

'''

