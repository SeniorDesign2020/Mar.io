import cv2
import os
import boto3
import shutil
import tqdm
from botocore.exceptions import NoCredentialsError
import zipfile
import progressbar
import shutil

def FrameCapture(file_name):
    folders = []
    vid = cv2.VideoCapture(file_name + '.mp4')
    os.mkdir('{}'.format(file_name))
    count = 0
    folderCount = 0
    success = 1
    while success:
        if count % 7200 == 0:
            folderCount += 1
            os.mkdir('{}/folder{}'.format(file_name,folderCount))
            folders.append('{}/folder{}'.format(file_name,folderCount))
        success, image = vid.read()
        try:
            cv2.imwrite('{}/folder{}/frame{}.jpg'.format(file_name,folderCount,count), image)
            count += 1
        except:
            continue
    
    zip_folders(folders)

    return folders

def zip_folders(folders):
    print('Zipping...')
    for folder in folders:
        shutil.make_archive('{}'.format(folder),'zip','{}'.format(folder))
        shutil.rmtree('{}'.format(folder))
        

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


def retrieve_file_paths(dirName):
 
  # setup file paths variable
  filePaths = []
   
  # Read all directory, subdirectories and file lists
  for root, directories, files in os.walk(dirName):
    for filename in files:
        # Create the full filepath by using os module.
        filePath = os.path.join(root, filename)
        filePaths.append(filePath)
         
  # return all paths
  return filePaths

def zip_dir(dir_name):
# Assign the name of the directory to zip
#   dir_name = 'mydir'
   
  # Call the function to retrieve all files and folders of the assigned directory
  filePaths = retrieve_file_paths(dir_name)

  # printing the list of all files to be zipped
#   print('The following list of files will be zipped:')
#   for fileName in filePaths:
#     print(fileName)
     
  # writing files to a zipfile
  zip_file = zipfile.ZipFile(dir_name+'.zip', 'w')
  with zip_file:
    # writing each file one by one
    for file in filePaths:
      zip_file.write(file)
       
  print(dir_name+'.zip file is created successfully!')


if __name__ == '__main__':

    file_name = input('video_name\n')
    keys = []
    if os.path.isfile('/home/seniordesign/Documents/srdesign/Mar.io/aws.txt'):
        with open('/home/seniordesign/Documents/srdesign/Mar.io/aws.txt','r') as in_file:
            line = in_file.readline()
            line = line.strip()
            ACCESS_KEY = line
            line = in_file.readline()
            line = line.strip()
            SECRET_KEY = line
    else:
        ACCESS_KEY = input('access_key\n')
        keys.append(ACCESS_KEY)
        SECRET_KEY = input('secret_key\n')
        keys.append(SECRET_KEY)
        with open('/home/seniordesign/Documents/srdesign/Mar.io/aws.txt','w') as out_file:
            for line in keys:
                out_file.write(line)
                out_file.write('\n')

    source = 'Videos/'
    destination = 'Frames'
    local_directory = file_name
    bucket = 'senior-design33'
    client = boto3.client('s3', aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY)
    #Download Video from AWS
    client.download_file(bucket, source + '{}.mp4'.format(file_name), '{}.mp4'.format(file_name))
    print('{}.mp4 downloaded to local'.format(file_name))

    #Video to Frames
    folders = FrameCapture(file_name)
    print('{}.mp4 converted to frames'. format(file_name))

    
    #Create Zip
    #zip_dir(file_name)
    
    #Upload to AWS w/ Progress Bar
    filesize = os.stat('{}'.format(file_name)).st_size
    print("\nuploading {} | size: {}".format(file_name, filesize))
    up_progress = progressbar.AnimatedProgressBar(end=filesize, width=50)
    def upload_progress(chunk):
        up_progress + chunk
        up_progress.show_progress()
    for folder in folders:
        client.upload_file('{}.zip'.format(folder), bucket, '{}/{}.zip'.format(destination,folder), Callback=upload_progress)
    print("\n{}.zip uploaded to S3 bucket:{} path:{}".format(file_name, bucket, destination))
    
    #Clean Up Local Directory
    
    clean = input("Clean Up Directory? (y/n): ")
    if clean == 'y':
        os.remove('{}.mp4'.format(file_name))
        #os.remove('{}'.format(file_name))
        shutil.rmtree(file_name)
        #shutil.rmtree('__pycache__')
    else:
        exit()
    
