from google_ref import Create_Service
from googleapiclient.errors import HttpError

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

try:
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    threads = service.users().threads().list(userId='me',q="after:2023/04/26").execute().get('threads', [])
    print(len(threads))
    for thread in threads:
        tdata = service.users().threads().get(userId='me', id=thread['id']).execute()
        nmsgs = len(tdata['messages'])
            # skip if <3 msgs in thread
        if nmsgs > 0:
            msg = tdata['messages'][0]['payload']
            subject = ''
            for header in msg['headers']:
                if header['name'] == 'Subject':
                    subject = header['value']
                    print("===================================================================================")
                    break
            if subject:
                print(F'- {subject}, {nmsgs}')

except HttpError as error:
        print(F'An error occurred: {error}')
        draft = None