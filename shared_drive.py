import sys
import pickle
import os.path
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

credentials_json = 'client_secrets.json'
credentials_pickle = 'token.pickle'


def get_creds():
    SCOPES = 'https://www.googleapis.com/auth/drive'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
        creds = tools.run_flow(flow, store)
    # DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    return creds


global creds


def main():
    # Build the drive service.
    drive_service = build('drive', 'v3', credentials=creds)

    # Get the drive ID of the first shared drive. You can introspect the
    # 'results' dict  here to get the right shared drive if it's not the first
    # one.
    results = drive_service.drives().list(pageSize=10).execute()
    shared_drive_id = results['drives'][0]['id']

    print(results)
    sys.exit()
    # Create the request metatdata, letting drive API know what it's receiving.
    # In this example, we place the image inside the shared drive root folder,
    # which has the same ID as the shared drive itself, but we could instead
    # choose the ID of a folder inside the shared drive.
    file_metadata = {
        'name': 'wakeupcat.jpg',
        'mimeType': 'image/jpeg',
        'parents': [shared_drive_id]}

    # Now create the media file upload object and tell it what file to upload,
    # in this case, "wakeupcat.jpg"
    media = MediaFileUpload('/path/to/wakeupcat.jpg', mimetype='image/jpeg')

    # Upload the file, making sure supportsAllDrives=True to enable uploading
    # to shared drives.
    f = drive_service.files().create(
        body=file_metadata, media_body=media, supportsAllDrives=True).execute()

    print("Created file '%s' id '%s'." % (f.get('name'), f.get('id')))
