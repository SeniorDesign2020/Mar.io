import os 
import boto3
from labeling_segment import filtering as fil
from Overlay import done
import cv2
from PIL import Image
from tqdm import tqdm
import shutil
import zipfile
import numpy as np


def labelling_zip(video_name, folder_name, s3_client):

    s3_client.download_file('senior-design33', 'Frames/{}/{}.zip'.format(video_name, folder_name), 'folder.zip')

    with zipfile.ZipFile('folder.zip','r') as in_file:
        for frame in tqdm(in_file.namelist()):
            try:

                frame_number = frame.split('.')[0]
                img_str = in_file.read(frame)
                img = cv2.imdecode(np.frombuffer(img_str, np.uint8), 1)
                cv2.imwrite('frame.jpg',img)
                filtered_image = fil('frame.jpg')
                image_cv2 = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB)
                image_pil = Image.fromarray(image_cv2)

                image_label = done(image_pil)
                image_label.save('{}/{}.jpg'.format(folder_name, frame_number))
            except Exception as e:
                print(e)
    os.remove('folder.zip')


def labelling_frames(video_name, folder_name, s3_client, bucket):
    paginator = s3_client.get_paginator('list_objects')
    operation_parameters = {'Bucket': bucket,
                            'Prefix': 'Frames/{}/{}'.format(video_name, folder_name)}
    pages = paginator.paginate(**operation_parameters)

    for page in pages:
        for obj in tqdm(page['Contents']):
            frame_number = obj['Key'].split('/')[-1]

            s3_client.download_file('senior-design33', obj['Key'], 'frame.jpg')
            try:
                filtered_image = fil('frame.jpg')
                image_cv2 = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB)
                image_pil = Image.fromarray(image_cv2)

                image_label = done(image_pil)
                image_label.save('{}/{}'.format(folder_name, frame_number))
            except:
                print('Cant label the frame {} \n Skipping for now'.format(frame_number))
                print('Go to aws console and check frame size, if zero the please delete')

def intialize_labelling():
    video_name = input('video_name\n')
    folder_name = input('folder_name\n')
    keys = []
    bucket = 'senior-design33'

    if os.path.isfile('aws.txt'):
        with open('aws.txt', 'r') as in_file:
            line = in_file.readline()
            line= line.strip()
            ACCESS_KEY = line
            line = in_file.readline()
            line=line.strip()
            SECRET_KEY = line
    else:
        ACCESS_KEY = input('access_key\n')
        keys.append(ACCESS_KEY)
        SECRET_KEY = input('secret_key\n')
        keys.append(SECRET_KEY)
        with open('aws.txt', 'w') as out_file:
            for line in keys:
                out_file.write(line)
                out_file.write("\n")
    if os.path.isdir(folder_name):
        shutil.rmtree(folder_name)
    else:
        os.mkdir('{}'.format(folder_name))

    s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    file = s3_client.list_objects(Bucket=bucket, Prefix='Frames/{}/{}'.format(video_name, folder_name))
    folder_type = file['Contents'][0]['Key'].split('/')[-1]
    is_zip = False
    if 'zip' in folder_type:
        is_zip = True
    if is_zip:
        labelling_zip(video_name, folder_name, s3_client)
    else:
        labelling_frames(video_name, folder_name, s3_client, bucket)

    shutil.make_archive('{}'.format(folder_name), 'zip', '{}'.format(folder_name))
    print('Uploading...')
    s3_client.upload_file('{}.zip'.format(folder_name), bucket, 'LabelledFrames/{}/{}.zip'.format(video_name,folder_name))
    shutil.rmtree('{}'.format(folder_name))
    os.remove('{}.zip'.format(folder_name))


if __name__ == '__main__':
    intialize_labelling()
