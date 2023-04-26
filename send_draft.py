from Google import Create_Service
import base64
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

try:

    mimeMessage = MIMEText("hello my name is ....")
    mimeMessage['To'] = 'bharadiyabhargav1234@gmail.com'
    mimeMessage['From'] = 'bharadiyabhargav1234@gmail.com'
    mimeMessage['Subject'] = 'You got files'

    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message=service.users().drafts().create(
        userId='me',
        body={'message':{'raw': raw_string }}
    ).execute()
    print(message)
    print("success create a draft mail.....!")

except HttpError as error:
        print(F'An error occurred: {error}')
        draft = None