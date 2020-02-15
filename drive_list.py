from __future__ import print_function

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/drive.appfolder'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

files = DRIVE.files().list().execute().get('files', [])
for f in files:
    print(f['name'], f['id'])

# results = DRIVE.drives().list(pageSize=10).execute()
# shared_drive_id = results['drives'][0]['id']
# print('Results are', results)
# # print(shared_drive_id)
