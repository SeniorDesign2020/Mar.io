import os
import botot3
from labeling_segment import filtering as fil
from Overlay import done
import cv2
from PIL import Image
from tqdm import tqdm

video_name = input('video_name')
folder_name = input('folder_name')

bucket = 'senior-design33'

destination = 'LabelledFrames'

'''
64os.mkdir('frames')
65bucket = 'senior-design33'
66client = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
67response = client.list_objects_v2(
68            Bucket=bucket,
69            Prefix ='Frames/{}'.format(filename),
70            MaxKeys=100 )
71
72for i,obj in enumerate(response['Contents']):
73    frame_number = obj['Key'].split('/')[-1]
74
75    client.download_file(bucket, obj['Key'], 'frames/{}'.format(frame_number))
76
77'''
