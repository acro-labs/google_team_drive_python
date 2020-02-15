from __future__ import print_function
import uuid

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

def create_td(td_name):
    request_id = str(uuid.uuid4()) # random unique UUID string
    body = {'name': td_name}
    return DRIVE.teamdrives().create(body=body,
            requestId=request_id, fields='id').execute().get('id')

def add_user(td_id, user, role='commenter'):
    body = {'type': 'user', 'role': role, 'emailAddress': user}
    return DRIVE.permissions().create(body=body, fileId=td_id,
            supportsTeamDrives=True, fields='id').execute().get('id')

def create_td_folder(td_id, folder):
    body = {'name': folder, 'mimeType': FOLDER_MIME, 'parents': [td_id]}
    return DRIVE.files().create(body=body,
            supportsTeamDrives=True, fields='id').execute().get('id')

def import_csv_to_td_folder(folder_id, fn, mimeType):
    body = {'name': fn, 'mimeType': mimeType, 'parents': [folder_id]}
    return DRIVE.files().create(body=body, media_body=fn+'.csv',
            supportsTeamDrives=True, fields='id').execute().get('id')

FOLDER_MIME = 'application/vnd.google-apps.folder'
SOURCE_FILE = 'Inventory' # on disk as 'inventory.csv'... CHANGE!
SHEETS_MIME = 'application/vnd.google-apps.spreadsheet'

td_id = create_td('AKROBAT Terapeut Team Drive')
print('** Team Drive created', td_id)
perm_id = add_user(td_id, 'martin@akrobatonline.dk') # CHANGE!
print('** User added to Team Drive', perm_id)
# folder_id = create_td_folder(td_id, ' Podio-pdf')
folder_id = '1aPWbieUO9lyyilBDiFsFURRhBZLm_j7-'
print('** Folder created in Team Drive', folder_id)
file_id = import_csv_to_td_folder(folder_id, SOURCE_FILE, SHEETS_MIME)
print('** CSV file imported as Google Sheets in Team Drives folder', file_id)

