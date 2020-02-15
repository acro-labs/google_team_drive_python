from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import googleapiclient, httplib2, oauth2client


import sys
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)


# Concurrent access made easy All calls made are thread-safe.
#The underlying implementation in the google-api-client library is not thread-safe,
#which means that every request has to re-authenticate an http object.
# You can avoid this overhead by creating your own http object for each thread and re-use it for every call.

# This can be done as follows:

# Create httplib.Http() object.
http = drive.auth.Get_Http_Object()

# Create file object to upload.
# # file_obj = drive.CreateFile()
# # file_obj['title'] = "file name"
# Upload the file and pass the http object into the call to Upload.
# file_obj.Upload(param={"http": http})

file1 = drive.CreateFile({'parents': ['0AErP3bqqT294Uk9PVA']})
file1.SetContentFile('photo.jpg')
file1.Upload(param={"http": http}) # Files.insert()

# You can specify the http-object in every access method which takes a param parameter
# File managment made easy
# file1['title'] = 'HelloWorld.txt'  # Change title of the file
# file1.Upload(param={"http": http}) # Files.patch()

# content = file1.GetContentString()  # 'Hello'
# file1.SetContentString(content+' World! - This file was created and uploaded with a python script!')  # 'Hello World!'
# file1.Upload(param={"http": http})

# Steps to get folder id


sys.exit()

file_list = drive.ListFile(
    {
        'q': "'root' in parents and trashed=false"
        
        }).GetList()
for file1 in file_list:       
    print ('title: %s, id: %s' % (file1['title'], file1['id'])) 
sys.exit()

# File managment made easy
file1['title'] = 'HelloWorld.txt'  # Change title of the file
file1.Upload() # Files.patch()

content = file1.GetContentString()  # 'Hello'
file1.SetContentString(content+' World!')  # 'Hello World!'
file1.Upload() # Files.update()

file2 = drive.CreateFile()
file2.SetContentFile('hello.png')
file2.Upload()
print('Created file %s with mimeType %s' % (file2['title'],
file2['mimeType']))
# Created file hello.png with mimeType image/png

file3 = drive.CreateFile({'id': file2['id']})
print('Downloading file %s from Google Drive' % file3['title']) # 'hello.png'
file3.GetContentFile('world.png')  # Save Drive file as a local file

# or download Google Docs files in an export format provided.
# downloading a docs document as an html file:
docsfile.GetContentFile('test.html', mimetype='text/html')
