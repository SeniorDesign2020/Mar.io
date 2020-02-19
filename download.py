import os 
import boto3

filename =  input('video_name\n')
folder_name = input('folder_name\n')

ACCESS_KEY = input('acces_key\n')

SECRET_KEY = input('secrete_key\n')




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



