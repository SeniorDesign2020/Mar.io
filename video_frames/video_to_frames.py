import cv2
import os
import boto3
from botocore.exceptions import NoCredentialsError

def FrameCapture(file_name):
    vid = cv2.VideoCapture(file_name + '.mp4')
    os.mkdir('{}'.format(file_name))
    count = 0
    folderCount = 0
    success = 1
    while success:
        if count % 7200 == 0:
            folderCount += 1
            os.mkdir('{}/folder{}'.format(file_name,folderCount))
        success, image = vid.read()
        cv2.imwrite('{}/folder{}/frame{}.jpg'.format(file_name,folderCount,count), image)
        count += 1

def upload_to_aws(client, local_directory, bucket, destination):
    for root, dirs, files in os.walk(local_directory):
        for filename in files:
            # construct the full local path
            local_path = os.path.join(root, filename)
            # construct the full Dropbox path
            relative_path = os.path.relpath(local_path, local_directory)
            s3_path = os.path.join(destination, relative_path)
            # relative_path = os.path.relpath(os.path.join(root, filename))
            print('Searching "%s" in "%s"' % (s3_path, bucket))
            try:
                client.head_object(Bucket=bucket, Key=s3_path)
                print("Path found on S3! Skipping %s..." % s3_path)

                # try:
                    # client.delete_object(Bucket=bucket, Key=s3_path)
                # except:
                    # print "Unable to delete %s..." % s3_path
            except:
                print("Uploading %s..." % s3_path)
                client.upload_file(local_path, bucket, s3_path)

if __name__ == '__main__':
    file_name = 'video_01-13-2020-lap2'

    ACCESS_KEY = 'AKIA6RPKPY2PO2ZALB5C'
    SECRET_KEY = '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'
    source = 'Videos/'
    destination = 'Frames/{}'.format(file_name)
    local_directory = file_name
    bucket = 'senior-design33'
    client = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)


    client.download_file(bucket, source + file_name + '.mp4', file_name + '.mp4')
    print('{}.mp4 downloaded to local'.format(file_name))
    FrameCapture(file_name)
    print('{}.mp4 converted to frames'. format(file_name))
    upload_to_aws(client, local_directory, bucket, destination)
    print('{} uploaded to AWS')