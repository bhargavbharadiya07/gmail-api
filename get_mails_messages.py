import os
import base64
import datetime
import calendar
from google_ref import Create_Service


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
    # print(message_details)
    return message_details


if __name__ == '__main__':
    m = 1
    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    t = datetime.datetime(2023, 4, 25, 17, 0, 0)
    date_time = calendar.timegm(t.timetuple()) - 19800
    query_string = f"after:{date_time}"
    save_location = "/home/bhargavpatel/silent/gmail-api/content/"
    email_messages = search_emails(query_string)

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
                if data == None or ('SENT' in messageDetail['labelIds']):
                    continue
                else:
                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    filepath = os.path.join(save_location, f'message{m}.txt')

                    with open(filepath, "wb") as file:
                        file.write(file_data)
                        print("success''''''!")
                        m += 1
                break
    print(m)
