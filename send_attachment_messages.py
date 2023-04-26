from google_ref import Create_Service
import base64
from email.message import EmailMessage
import mimetypes
from googleapiclient.errors import HttpError


CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

try:
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    mimeMessage = EmailMessage()
    mimeMessage['To'] = 'bharadiyabhargav1234@gmail.com'
    mimeMessage['From'] = 'bharadiyabhargav1234@gmail.com'
    mimeMessage['Subject'] = 'You got files'
    print("success full print....!")
    mimeMessage.set_content('hello i am  attach a images.')

    # attachment
    attachment_filenames = ['photo.jpg']

    # guessing the MIME type
    for attachment_filename in attachment_filenames:
        type_subtype,_= mimetypes.guess_type(attachment_filename)
        maintype,subtype = type_subtype.split('/')

        with open(attachment_filename, 'rb') as fp:
            attachment_data = fp.read()
        mimeMessage.add_attachment(attachment_data, maintype, subtype)

    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    content={
        'raw':raw_string
    }

    message = (service.users().messages().send(
        userId='me',
        body=content).execute())
    print(message)

except HttpError as error:
        print(F'An error occurred: {error}')
        draft = None