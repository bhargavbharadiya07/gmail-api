import os
import base64
import time
from google_ref import Create_Service

def search_emails(query_string: str, label_ids: list = None):
    try:
        message_list_response = service.users().messages().list(
            userId='me',
            labelIds=label_ids,
            q=query_string,
        ).execute()

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
    m = 1
    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    query_string ="is:important"

    save_location = "/home/bhargavpatel/silent/gmail-api/content/"
    email_messages = search_emails(query_string)

    # print(email_messages)
    for email_message in email_messages:
        print("======================================================================")
        messageDetail = get_message_detail(email_message['id'], msg_format='full', metadata_headers=['parts'])
        messagesDetailPayload = messageDetail.get('payload')

        if 'parts' in messagesDetailPayload:

            for msgPayload in messagesDetailPayload['parts']:
                file_name = msgPayload['filename']
                partId=msgPayload.get('partId')
                body = msgPayload['body']

                if 'attachmentId' in body:
                    attachment_id = body['attachmentId']
                    attachment_content = get_file_data(email_message['id'], attachment_id, file_name, save_location)
                    print(attachment_content)
                    filepath = os.path.join(save_location,file_name)

                    if file_name == '':
                        pass
                    else:
                        with open(filepath, "wb") as file:
                            file.write(attachment_content)
                            print("success''''''!")
        m += 1
        time.sleep(0.1)
    print(m)
