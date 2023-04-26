import os
import base64
import datetime
from dateutil.relativedelta import relativedelta

import calendar
from google_ref import Create_Service
import threading

def search_emails(query_string: str, label_ids: list = None):
    try:
        message_list_response = service.users().messages().list(
            userId='me',
            labelIds=label_ids,
            q=query_string,
        ).execute()
        print("=============================================================================================================")
        message_items = message_list_response.get('messages')

        next_page_token = message_list_response.get('nextPageToken')
        while next_page_token:
            message_list_response = service.users().messages().list(
                userId='me',
                labelIds=label_ids,
                q=query_string,
                pageToken=next_page_token
            ).execute()
            message_items.extend(message_list_response.get('messages'))
            next_page_token = message_list_response.get('nextPageToken')
            print(next_page_token)
        return message_items

    except Exception as e:
        raise print('No emails returned')

def get_file_data(message_id, attachment_id, file_name, save_Location):
    response = service.users().messages().attachments().get(
        userId='me',
        messageId=message_id,
        id=attachment_id
    ).execute()

    file_data = base64.urlsafe_b64decode(response.get('data').encode('UTF-8'))
    return file_data


def get_message_detail(message_id, msg_format='metadata', metadata_headers: list = None):
    message_details = service.users().messages().get(
        userId='me',
        id=message_id,
        format=msg_format,
        metadataHeaders=metadata_headers
    ).execute()
    return message_details


if __name__ == '__main__':

    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    def doSomething():
        m = 1
        print("hello")
        tz = datetime.datetime.now()
        t = datetime.timedelta(minutes=1)
        ti = tz - t
        date_time = calendar.timegm(ti.timetuple()) - 19800
        print(ti.strftime("%Y-%m-%d %H:%M:%S"))

        query_string = f"after:{date_time}"
        save_location = "/home/bhargavpatel/silent/gmail-api/content/"
        email_messages = search_emails(query_string)

        if email_messages == None :
            exit()
        for email_message in email_messages:

            messageDetail = get_message_detail(email_message['id'], msg_format='full', metadata_headers=['parts'])
            print(messageDetail)

            messagesDetailPayload = messageDetail.get('payload')

            if 'parts' in messagesDetailPayload:
                for msgPayload in messagesDetailPayload['parts']:
                    file_name = msgPayload['filename']
                    partId = msgPayload.get('partId')
                    body = msgPayload['body']
                    data = body.get('data')
                    if data == None or ('INBOX' in messageDetail['labelIds']):
                        continue
                    else:
                        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                        filepath = os.path.join(save_location, f'message{m}.txt')

                        with open(filepath, "wb") as file:
                            file.write(file_data)
                            print("success''''''!")
                    break
            m += 1

        print(m)

    def set_interval(func, sec):
        def func_wrapper():
            set_interval(func, sec)
            func()
        t = threading.Timer(sec, func_wrapper)
        t.start()
        return t
    set_interval(doSomething, 60)


