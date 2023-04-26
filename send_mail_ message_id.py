from google_ref import Create_Service
import base64
from email.mime.text import MIMEText
from email.message import EmailMessage
from googleapiclient.errors import HttpError

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
try:

    # ==================================send mail with message id ===================================

    mimeMessage = MIMEText("hello my name is ....")

    message_id = 'CAE04LQNDNVPbk22-jRp6UsJ2OWiFHBtpcUfF4U+w6rRm_e68DQ@mail.gmail.com'
    mimeMessage['To'] = 'bhargav.silentinfotech@gmail.com'
    mimeMessage['From'] = 'bhargav.silentinfotech@gmail.com'
    mimeMessage['Subject'] = 'You got files'
    mimeMessage['In-Reply-To'] = f'<{message_id}>'
    mimeMessage['References'] = f'<{message_id}>'

    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    print(raw_string)

    messages = service.users().messages().send(
        userId='me',
        body={'raw': raw_string}).execute()
    print(messages)

except HttpError as error:
        print(F'An error occurred: {error}')
        draft = None